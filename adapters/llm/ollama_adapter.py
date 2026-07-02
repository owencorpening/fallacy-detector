import json
import urllib.request

from adapters.llm.base import LLMAdapter
from core.classifier import build_batch_prompt, build_prompt, parse_batch_response, parse_response
from core.fallacies import FallacyResult


class OllamaAdapter(LLMAdapter):
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self._model = model
        self._url = f"{base_url}/api/chat"

    def _chat(self, prompt: str) -> str:
        payload = json.dumps({
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }).encode()
        req = urllib.request.Request(
            self._url,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())["message"]["content"]

    def classify(self, transcript: str, context: list[str]) -> FallacyResult | None:
        return parse_response(self._chat(build_prompt(transcript, context)), transcript)

    def classify_all(self, transcript: str) -> list[FallacyResult]:
        return parse_batch_response(self._chat(build_batch_prompt(transcript)), transcript)
