from abc import ABC, abstractmethod
from core.fallacies import FallacyResult


class LLMAdapter(ABC):
    @abstractmethod
    def classify(self, transcript: str, context: list[str]) -> FallacyResult | None:
        """Classify a single chunk for fallacies (realtime mode)."""
        ...

    @abstractmethod
    def classify_all(self, transcript: str) -> list[FallacyResult]:
        """Classify a full transcript for all fallacies (batch mode)."""
        ...
