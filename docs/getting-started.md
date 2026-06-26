# Getting started

## Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/) (free tier works)
- A working microphone (for live input) or an audio file to test with

## Install

```bash
git clone <repo-url>
cd fallacy-detector
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

`faster-whisper` will download the Whisper model on first run (~75 MB for `tiny`). This is cached locally and only happens once.

## Set your API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Add that to your shell profile (`~/.bashrc`, `~/.zshrc`) to avoid re-entering it each session.

## First run

```bash
.venv/bin/python main.py
```

The tool starts listening on your default microphone. Speak a sentence — try something like:

> "If you don't support this policy, you clearly don't care about the country."

After a few seconds you should see:

```
[FALSE DICHOTOMY 0.89] "if you don't support this policy, you clearly don't care about the country"
```

Nothing is printed for clean audio. `Ctrl+C` to stop.

## Test with a file instead

If you don't want to use your mic, point it at a local audio file:

```bash
.venv/bin/python main.py --source file --file path/to/audio.mp3
```

Supported formats: anything `ffmpeg` can decode (mp3, wav, m4a, ogg, flac, etc.).

## Test with a YouTube URL

Pass any public YouTube URL to analyze it without downloading:

```bash
.venv/bin/python main.py --source youtube --url "https://www.youtube.com/watch?v=..."
```

Audio streams in real time — output appears chunk by chunk as it plays through.

## Troubleshooting

**No output at all** — the audio may be clean. Try speaking more clearly, or lower the Whisper model size check (`tiny` sometimes misses quieter speech — try `base` in `config.yaml`).

**`sounddevice` error on startup** — your system may need `portaudio`:
```bash
sudo apt install portaudio19-dev   # Ubuntu/Debian
brew install portaudio             # macOS
```

**Slow first response** — the Whisper model loads into memory on the first chunk. Subsequent chunks are faster.

**API key error** — confirm the variable is exported in the current shell session: `echo $ANTHROPIC_API_KEY`.

## Next steps

- [Config reference](config.md) — tune chunk size, switch models, change providers
- [Use cases](use-cases.md) — YouTube, streams, meetings, offline files
- [Extending](extending.md) — add your own fallacies or swap in a different LLM
