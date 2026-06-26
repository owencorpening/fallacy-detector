import numpy as np
from faster_whisper import WhisperModel
from adapters.stt.base import STTAdapter


class WhisperLocalAdapter(STTAdapter):
    def __init__(self, model_size: str = "tiny"):
        self._model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio_chunk: np.ndarray) -> str:
        segments, _ = self._model.transcribe(audio_chunk, vad_filter=True)
        return " ".join(seg.text.strip() for seg in segments).strip()
