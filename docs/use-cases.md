# Use cases

## Live debate or speech monitoring

Point the tool at your microphone while watching a debate, political speech, or press conference in the same room.

```bash
.venv/bin/python main.py --source mic
```

For better pickup of audio playing from speakers, route system audio to a virtual mic (e.g. PulseAudio loopback on Linux, Blackhole on macOS) and set that as your default input device.

## Analyze a YouTube video

Pass a YouTube URL directly. `yt-dlp` downloads and pipes the audio; no file is saved.

```bash
.venv/bin/python main.py --source youtube --url "https://www.youtube.com/watch?v=..."
```

This works on most public videos, including long-form content. The video plays through at normal speed — use a longer `chunk_seconds` if the speech is dense.

## Analyze a local recording

Run it against any audio or video file on disk:

```bash
.venv/bin/python main.py --source file --file recording.mp3
.venv/bin/python main.py --source file --file interview.wav
.venv/bin/python main.py --source file --file lecture.m4a
```

Processing runs at roughly real-time speed — a 10-minute file takes about 10 minutes. To save the output:

```bash
.venv/bin/python main.py --source file --file lecture.m4a > fallacies.txt
```

## Monitor a live stream

Any HTTP audio stream URL works with `--source stream`:

```bash
.venv/bin/python main.py --source stream --url "http://stream.example.com/live.mp3"
```

Useful for radio streams, podcast live feeds, or any continuous audio URL.

## Batch processing multiple files

Wrap the tool in a shell loop to process a folder:

```bash
for f in recordings/*.mp3; do
  echo "=== $f ===" >> output.txt
  .venv/bin/python main.py --source file --file "$f" >> output.txt
done
```

## Educational use

Paste a debate transcript into a text file and route it through a TTS engine, or just use a recording. The output is structured enough to parse and score:

```bash
.venv/bin/python main.py --source file --file debate.wav | sort | uniq -c | sort -rn
```

That gives a ranked frequency count of which fallacies appeared most.

## Reducing cost on long content

The default model (`claude-haiku-4-5-20251001`) is fast and cheap. For long recordings where accuracy matters more than cost:

```yaml
# config.yaml
llm:
  provider: anthropic
  model: claude-sonnet-4-6
```

For offline / zero-API-cost operation, use OpenAI-compatible local inference endpoints that accept the same request format.

## Increasing accuracy for noisy audio

Switch Whisper to a larger model for difficult audio conditions:

```yaml
# config.yaml
stt:
  provider: whisper-local
  model_size: small   # or medium for heavily accented/noisy speech
```

Increase `chunk_seconds` if speech is slow or has long pauses between thoughts:

```yaml
pipeline:
  chunk_seconds: 10
  context_window: 5
```
