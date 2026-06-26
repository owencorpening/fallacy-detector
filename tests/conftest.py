import wave
import struct
import numpy as np
import pytest

from adapters.llm.base import LLMAdapter
from adapters.stt.base import STTAdapter
from core.fallacies import FallacyResult


def make_wav(path: str, duration_seconds: float = 10.0, sample_rate: int = 16000) -> None:
    n = int(duration_seconds * sample_rate)
    samples = (np.sin(2 * np.pi * 440 * np.arange(n) / sample_rate) * 8000).astype(np.int16)
    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(samples.tobytes())


@pytest.fixture
def audio_file(tmp_path):
    path = str(tmp_path / "test.wav")
    make_wav(path, duration_seconds=12.0)
    return path


@pytest.fixture
def short_audio_file(tmp_path):
    path = str(tmp_path / "short.wav")
    make_wav(path, duration_seconds=3.0)
    return path


class FixedSTT(STTAdapter):
    def __init__(self, text: str):
        self._text = text

    def transcribe(self, audio_chunk: np.ndarray) -> str:
        return self._text


class FixedLLM(LLMAdapter):
    def __init__(self, result: FallacyResult | None):
        self._result = result
        self.calls: list[tuple[str, list[str]]] = []

    def classify(self, transcript: str, context: list[str]) -> FallacyResult | None:
        self.calls.append((transcript, context))
        return self._result


@pytest.fixture
def straw_man_result():
    return FallacyResult(
        name="Straw Man",
        confidence=0.91,
        trigger_phrase="so you're saying we should ban everything",
    )
