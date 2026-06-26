from adapters.llm.base import LLMAdapter
from core.fallacies import FallacyResult


class OpenAIAdapter(LLMAdapter):
    """Stub — not yet implemented."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        raise NotImplementedError("OpenAI LLM adapter is not yet implemented")

    def classify(self, transcript: str, context: list[str]) -> FallacyResult | None:
        raise NotImplementedError
