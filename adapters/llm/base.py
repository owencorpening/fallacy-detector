from abc import ABC, abstractmethod
from core.fallacies import FallacyResult


class LLMAdapter(ABC):
    @abstractmethod
    def classify(self, transcript: str, context: list[str]) -> FallacyResult | None:
        """Classify transcript for fallacies given sliding context window."""
        ...
