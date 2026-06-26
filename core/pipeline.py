import collections
import threading
import numpy as np

from adapters.llm.base import LLMAdapter
from adapters.stt.base import STTAdapter
from transport.base import AudioSource


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

    def run(self) -> None:
        for chunk in self._source.chunks():
            threading.Thread(target=self._process, args=(chunk,), daemon=True).start()

    def _process(self, audio: np.ndarray) -> None:
        transcript = self._stt.transcribe(audio)
        if not transcript:
            return

        result = self._llm.classify(transcript, list(self._context))
        self._context.append(transcript)

        if result:
            print(str(result), flush=True)
