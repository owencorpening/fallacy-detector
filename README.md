# fallacy-detector

Real-time CLI tool that listens to audio, transcribes it, and flags logical fallacies as they happen.

```text
[STRAW MAN 0.87] "so you're saying we should just ban everything"
[AD HOMINEM 0.91] "why would we listen to her — she went bankrupt twice"
```

Audio comes from a microphone, local file, HTTP stream, or YouTube URL. Transcription runs locally via Whisper (or OpenAI's API). Classification runs through Claude or GPT. All three are swappable via `config.yaml`.

## Quick start

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/python main.py                   # mic input, default config
```

## Audio sources

| Source | Flag | Example |
| ------ | ---- | ------- |
| Microphone (default) | `--source mic` | `.venv/bin/python main.py` |
| Local file | `--source file --file path/to/audio.wav` | `.venv/bin/python main.py --source file --file debate.mp3` |
| HTTP stream | `--source stream --url <url>` | `.venv/bin/python main.py --source stream --url http://...` |
| YouTube | `--source youtube --url <url>` | `.venv/bin/python main.py --source youtube --url https://youtu.be/...` |

## Configuration

All options live in `config.yaml`. The defaults use local Whisper (`tiny` model) and Anthropic Claude Haiku — fast and free-tier friendly.

```yaml
stt:
  provider: whisper-local   # whisper-local | openai-whisper
  model_size: tiny

llm:
  provider: anthropic       # anthropic | openai
  model: claude-haiku-4-5-20251001
  api_key: ${ANTHROPIC_API_KEY}

pipeline:
  chunk_seconds: 5
  context_window: 3
  sample_rate: 16000
```

Pass a different config file with `--config myconfig.yaml`.

See [docs/config.md](docs/config.md) for the full reference.

## Fallacies detected

Straw Man, Ad Hominem, False Dichotomy, Slippery Slope, Appeal to Authority, Hasty Generalization, Circular Reasoning, Red Herring, Appeal to Emotion, Bandwagon.

Definitions and examples: [docs/fallacies.md](docs/fallacies.md)

## Docs

- [Getting started](docs/getting-started.md) — install, first run, troubleshooting
- [Use cases](docs/use-cases.md) — YouTube, streams, files, batch processing
- [Architecture](docs/architecture.md) — how the pipeline works
- [Config reference](docs/config.md) — all config options
- [Fallacies](docs/fallacies.md) — what's detected and how
- [Extending](docs/extending.md) — adding providers and fallacies
