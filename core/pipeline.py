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
