from abc import ABC, abstractmethod
import numpy as np


class STTAdapter(ABC):
    @abstractmethod
    def transcribe(self, audio_chunk: np.ndarray) -> str:
        """Transcribe a numpy audio array (float32, 16kHz mono) to text."""
        ...
