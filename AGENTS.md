# AGENTS.md — fallacy-detector

Real-time CLI tool that listens to audio, transcribes it, and detects logical fallacies.

## Python Environment

This project uses a local venv at `.venv/`. Always use it — never the system Python.

```bash
# install / sync deps
.venv/bin/pip install -r requirements.txt

# run
.venv/bin/python main.py

# test
.venv/bin/python -m pytest tests/
```

If `.venv/` does not exist yet: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`

**VS Code:** select the venv interpreter to silence "package not found" warnings — `Ctrl+Shift+P` → *Python: Select Interpreter* → `.venv/bin/python`.

## Architecture

Adapter pattern throughout — all providers are swappable via `config.yaml`.

```
fallacy-detector/
  adapters/
    llm/           # LLMAdapter base + anthropic_adapter, openai_adapter (stub)
    stt/           # STTAdapter base + whisper_local, openai_whisper (stub)
  core/
    pipeline.py    # audio capture → STT → LLM → stdout
    fallacies.py   # FallacyDefinition, FallacyResult, top-10 definitions + examples
    classifier.py  # prompt builder + response parser
  config.yaml      # active providers, model sizes, chunk_seconds
  main.py          # CLI entry point
```

## Running

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
python main.py                        # uses config.yaml defaults
python main.py --config myconfig.yaml
```

Output: one line per detected fallacy, suppressed if clean.
```
[STRAW MAN 0.87] "so you're saying we should just ban everything"
```

## Extending

### Add a new LLM provider
1. Create `adapters/llm/myprovider_adapter.py` subclassing `LLMAdapter`
2. Implement `classify(transcript, context) → FallacyResult | None`
3. Add the provider name to `build_llm()` in `main.py`
4. Set `llm.provider: myprovider` in `config.yaml`

### Add a new STT provider
1. Create `adapters/stt/myprovider.py` subclassing `STTAdapter`
2. Implement `transcribe(audio_chunk: np.ndarray) → str`
3. Add the provider name to `build_stt()` in `main.py`
4. Set `stt.provider: myprovider` in `config.yaml`

### Add or tune fallacies
Edit `core/fallacies.py` — the `FALLACIES` list drives both the prompt and the parser.

## Config reference

```yaml
stt:
  provider: whisper-local   # whisper-local | openai-whisper
  model_size: tiny          # tiny | base | small | medium | large

llm:
  provider: anthropic       # anthropic | openai
  model: claude-haiku-4-5-20251001
  api_key: ${ANTHROPIC_API_KEY}

pipeline:
  chunk_seconds: 5          # audio window per inference call
  context_window: 3         # previous chunks fed to LLM for continuity
  sample_rate: 16000
```

## Fallacies detected

Straw Man, Ad Hominem, False Dichotomy, Slippery Slope, Appeal to Authority,
Hasty Generalization, Circular Reasoning, Red Herring, Appeal to Emotion, Bandwagon.
