import anthropic
from adapters.llm.base import LLMAdapter
from core.classifier import build_prompt, parse_response
from core.fallacies import FallacyResult


class AnthropicAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "claude-haiku-4-5-20251001"):
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    def classify(self, transcript: str, context: list[str]) -> FallacyResult | None:
        prompt = build_prompt(transcript, context)
        message = self._client.messages.create(
            model=self._model,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text
        return parse_response(raw)
