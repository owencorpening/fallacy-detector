# Config reference

All configuration lives in `config.yaml` (or a file passed via `--config`).

## `stt` — Speech-to-text

```yaml
stt:
  provider: whisper-local   # required
  model_size: tiny          # whisper-local only
  api_key: ${OPENAI_API_KEY}  # openai-whisper only
  model: whisper-1            # openai-whisper only
```

| Key | Default | Description |
|-----|---------|-------------|
| `provider` | `whisper-local` | `whisper-local` or `openai-whisper` |
| `model_size` | `tiny` | Whisper model size: `tiny` `base` `small` `medium` `large` |
| `api_key` | — | OpenAI API key (env var reference or literal). Required for `openai-whisper`. |
| `model` | `whisper-1` | OpenAI model name. Used only with `openai-whisper`. |

**Whisper model tradeoffs:**

| Size | Speed | Accuracy | VRAM |
|------|-------|----------|------|
| `tiny` | fastest | lowest | ~1 GB |
| `base` | fast | decent | ~1 GB |
| `small` | moderate | good | ~2 GB |
| `medium` | slow | very good | ~5 GB |
| `large` | slowest | best | ~10 GB |

`tiny` works well for clear speech. Use `small` or `base` for noisy environments or accented speech.

## `llm` — Language model

```yaml
llm:
  provider: anthropic         # required
  model: claude-haiku-4-5-20251001
  api_key: ${ANTHROPIC_API_KEY}
```

| Key | Default | Description |
|-----|---------|-------------|
| `provider` | `anthropic` | `anthropic` or `openai` |
| `model` | `claude-haiku-4-5-20251001` | Model name passed to the API |
| `api_key` | `${ANTHROPIC_API_KEY}` | API key. Supports `${ENV_VAR}` syntax. |

**Provider notes:**
- `anthropic` — Claude models. Haiku is fastest and cheapest; use Sonnet for higher accuracy.
- `openai` — GPT models. `gpt-4o-mini` is the cheapest option.

## `pipeline` — Chunk and context settings

```yaml
pipeline:
  chunk_seconds: 5
  context_window: 3
  sample_rate: 16000
```

| Key | Default | Description |
|-----|---------|-------------|
| `chunk_seconds` | `5` | Length of each audio chunk fed to STT |
| `context_window` | `3` | Number of previous transcripts included in the LLM prompt |
| `sample_rate` | `16000` | Audio sample rate in Hz. Whisper expects 16000. |

**Tuning tips:**
- Shorter `chunk_seconds` gives lower latency but may cut sentences mid-thought, reducing accuracy.
- Longer `chunk_seconds` gives the LLM more context per call but increases end-to-end delay.
- `context_window: 0` disables context; each chunk is classified in isolation.

## Environment variables

API keys can be referenced as `${VAR_NAME}` anywhere in the config. The value is resolved at startup; if the variable is unset, the program exits with an error message.

```yaml
llm:
  api_key: ${ANTHROPIC_API_KEY}
```

You can also set the key literally (not recommended for shared configs):

```yaml
llm:
  api_key: sk-ant-...
```
