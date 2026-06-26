import numpy as np
from adapters.stt.base import STTAdapter


class OpenAIWhisperAdapter(STTAdapter):
    """Stub — not yet implemented."""

    def __init__(self, api_key: str, model: str = "whisper-1"):
        raise NotImplementedError("OpenAI Whisper adapter is not yet implemented")

    def transcribe(self, audio_chunk: np.ndarray) -> str:
        raise NotImplementedError
