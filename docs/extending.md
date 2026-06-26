# Extending the detector

## Add a new LLM provider

1. Create `adapters/llm/myprovider_adapter.py`:

```python
from adapters.llm.base import LLMAdapter
from core.classifier import build_prompt, parse_response
from core.fallacies import FallacyResult


class MyProviderAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str):
        self._client = MyProviderClient(api_key=api_key)
        self._model = model

    def classify(self, transcript: str, context: list[str]) -> FallacyResult | None:
        prompt = build_prompt(transcript, context)
        response = self._client.complete(model=self._model, prompt=prompt)
        return parse_response(response.text)
```

2. Register it in `main.py` inside `build_llm()`:

```python
elif provider == "myprovider":
    from adapters.llm.myprovider_adapter import MyProviderAdapter
    return MyProviderAdapter(
        api_key=resolve_env(cfg["api_key"]),
        model=cfg.get("model", "my-default-model"),
    )
```

3. Set it in `config.yaml`:

```yaml
llm:
  provider: myprovider
  model: my-model-name
  api_key: ${MY_PROVIDER_API_KEY}
```

## Add a new STT provider

1. Create `adapters/stt/myprovider.py`:

```python
import numpy as np
from adapters.stt.base import STTAdapter


class MySTTAdapter(STTAdapter):
    def __init__(self, api_key: str):
        self._client = MySTTClient(api_key=api_key)

    def transcribe(self, audio: np.ndarray) -> str:
        # audio is float32, 16kHz, mono
        result = self._client.transcribe(audio)
        return result.text or ""
```

2. Register it in `main.py` inside `build_stt()`:

```python
elif provider == "mystt":
    from adapters.stt.myprovider import MySTTAdapter
    return MySTTAdapter(api_key=resolve_env(cfg["api_key"]))
```

3. Set it in `config.yaml`:

```yaml
stt:
  provider: mystt
  api_key: ${MY_STT_API_KEY}
```

## Add a new audio source

1. Create `transport/mysource.py`:

```python
from collections.abc import Iterator
import numpy as np
from transport.base import AudioSource


class MyAudioSource(AudioSource):
    def __init__(self, chunk_seconds: int = 5, sample_rate: int = 16000):
        self._chunk_seconds = chunk_seconds
        self._sample_rate = sample_rate

    def chunks(self) -> Iterator[np.ndarray]:
        # yield float32 mono arrays of length (chunk_seconds * sample_rate)
        while True:
            yield self._get_next_chunk()
```

2. Register it in `main.py` inside `build_source()`:

```python
elif source == "mysource":
    from transport.mysource import MyAudioSource
    return MyAudioSource(chunk_seconds=chunk_seconds, sample_rate=sample_rate)
```

3. Add it to the `--source` choices in the argparse block:

```python
parser.add_argument("--source", choices=["file", "stream", "youtube", "mic", "mysource"])
```

## Add or tune fallacies

All fallacy definitions live in `core/fallacies.py` in the `FALLACIES` list. Each entry is a `FallacyDefinition`:

```python
FallacyDefinition(
    name="My Fallacy",
    description="One sentence describing the pattern.",
    examples=[
        "Example A — the fallacious claim.",
        "Example B — another form of it.",
    ],
)
```

The `FALLACIES` list drives both the LLM prompt and the response parser. No other files need changing. Adding strong, concrete examples improves detection accuracy more than tweaking descriptions.
