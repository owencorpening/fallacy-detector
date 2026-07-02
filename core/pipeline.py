import collections
import sys
import threading
import time
import numpy as np

from adapters.llm.base import LLMAdapter
from adapters.stt.base import STTAdapter
from transport.base import AudioSource


def _err(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def _dot_progress(label: str, stop: threading.Event) -> None:
    print(label, end="", file=sys.stderr, flush=True)
    while not stop.wait(3.0):
        print(".", end="", file=sys.stderr, flush=True)
    print("", file=sys.stderr)


class Pipeline:
    def __init__(
        self,
        source: AudioSource,
        stt: STTAdapter,
        llm: LLMAdapter,
        context_window: int = 3,
    ):
        self._source = source
        self._stt = stt
        self._llm = llm
        self._context: collections.deque[str] = collections.deque(maxlen=context_window)
        self._seen: collections.deque[str] = collections.deque(maxlen=10)
        self._stop = threading.Event()

    def run(self) -> None:
        _err("Listening... (Ctrl+C to stop)")
        for chunk in self._source.chunks():
            if self._stop.is_set():
                break
            transcript = self._stt.transcribe(chunk)
            if transcript:
                _err(f"  > {transcript}")
                threading.Thread(target=self._classify, args=(transcript,), daemon=True).start()

    def run_batch(self) -> None:
        chunks: list[str] = []
        stop = threading.Event()
        t = threading.Thread(target=_dot_progress, args=("Transcribing", stop), daemon=True)
        t.start()
        try:
            for chunk in self._source.chunks():
                transcript = self._stt.transcribe(chunk)
                if transcript:
                    chunks.append(transcript)
        except KeyboardInterrupt:
            pass
        finally:
            stop.set()
            t.join()

        if not chunks:
            _err("No speech detected.")
            return

        full = " ".join(chunks)
        stop2 = threading.Event()
        t2 = threading.Thread(target=_dot_progress, args=("Analyzing", stop2), daemon=True)
        t2.start()
        try:
            results = self._llm.classify_all(full)
        except Exception as e:
            stop2.set()
            t2.join()
            _err(f"Error: {e}")
            return
        finally:
            stop2.set()
            t2.join()

        seen: set[str] = set()
        for result in results:
            key = f"{result.name}:{result.trigger_phrase.lower()}"
            if key not in seen:
                seen.add(key)
                print(str(result), flush=True)

    def _classify(self, transcript: str) -> None:
        t0 = time.monotonic()
        try:
            result = self._llm.classify(transcript, list(self._context))
        except Exception as e:
            _err(f"Error: {e}")
            self._stop.set()
            return

        elapsed = time.monotonic() - t0
        _err(f"  ({elapsed:.1f}s)")
        self._context.append(transcript)
        if result:
            key = f"{result.name}:{result.trigger_phrase.lower()}"
            if key not in self._seen:
                self._seen.append(key)
                print(str(result), flush=True)
