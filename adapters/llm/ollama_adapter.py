import json
import urllib.request

from adapters.llm.base import LLMAdapter
from core.classifier import build_prompt, parse_response
from core.fallacies import FallacyResult


class OllamaAdapter(LLMAdapter):
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self._model = model
        self._url = f"{base_url}/api/chat"

    def classify(self, transcript: str, context: list[str]) -> FallacyResult | None:
        prompt = build_prompt(transcript, context)
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
            data = json.loads(resp.read())

        raw = data["message"]["content"]
        return parse_response(raw, transcript)
