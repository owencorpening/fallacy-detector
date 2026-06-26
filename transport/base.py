from abc import ABC, abstractmethod
from collections.abc import Iterator
import numpy as np


class AudioSource(ABC):
    @abstractmethod
    def chunks(self) -> Iterator[np.ndarray]:
        """Yields float32 16kHz mono audio chunks."""
        ...
