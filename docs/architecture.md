# Architecture

## Overview

```
Audio source → STT adapter → LLM adapter → stdout
       ↑              ↑             ↑
  transport/      adapters/stt/ adapters/llm/
```

The pipeline pulls fixed-length audio chunks from a source, transcribes each chunk, then asks the LLM to classify it. Each chunk is processed in its own thread so audio capture never stalls waiting for inference.

## Components

### Transport layer (`transport/`)

Audio sources implement `AudioSource.chunks()`, which yields `float32` 16 kHz mono NumPy arrays. Four sources ship out of the box:

| Class | File | Description |
|-------|------|-------------|
| `MicrophoneAudioSource` | `transport/microphone.py` | Live mic via `sounddevice` |
| `FileAudioSource` | `transport/file.py` | Local audio file |
| `StreamURLAudioSource` | `transport/stream_url.py` | HTTP audio stream |
| `YouTubeAudioSource` | `transport/youtube.py` | YouTube URL via `yt-dlp` |

### STT adapters (`adapters/stt/`)

`STTAdapter.transcribe(chunk: np.ndarray) → str` — takes a chunk, returns a transcript string (empty string if nothing audible).

| Adapter | Key dep | Notes |
|---------|---------|-------|
| `WhisperLocalAdapter` | `faster-whisper` | Runs on-device; default |
| `OpenAIWhisperAdapter` | `openai` | Calls the Whisper API |

### LLM adapters (`adapters/llm/`)

`LLMAdapter.classify(transcript, context) → FallacyResult | None` — sends the transcript plus recent context to the model and returns a parsed result or `None` if clean.

| Adapter | Key dep | Notes |
|---------|---------|-------|
| `AnthropicAdapter` | `anthropic` | Uses Claude; default |
| `OpenAIAdapter` | `openai` | Uses GPT models |

### Core (`core/`)

| Module | Responsibility |
|--------|----------------|
| `pipeline.py` | Orchestrates chunk → STT → LLM → print loop |
| `classifier.py` | Builds the LLM prompt; parses JSON response |
| `fallacies.py` | `FallacyDefinition` list + `FallacyResult` dataclass |

### Entry point (`main.py`)

Parses CLI args, reads `config.yaml`, wires up the chosen source/STT/LLM, and calls `Pipeline.run()`.

## Data flow

```
1. AudioSource.chunks()
      yields np.ndarray (float32, 16kHz, mono)

2. Pipeline._process(chunk)  [in a daemon thread]
      transcript = STTAdapter.transcribe(chunk)
      result = LLMAdapter.classify(transcript, context_deque)
      context_deque.append(transcript)

3. If result is not None:
      print(str(result))   →  "[STRAW MAN 0.87] \"quote\""
```

## Context window

The pipeline keeps a rolling deque of the last N transcripts (`context_window` in config). Each LLM call receives the current transcript plus those previous ones, so the classifier can spot fallacies that span sentence boundaries.

## Threading model

`Pipeline.run()` starts a new daemon thread per chunk. The main thread stays blocked on `AudioSource.chunks()` (which is a blocking generator). Threads share `_context` but only the append operation is performed after the classify call, so interleaving is bounded and low-risk for the use case.
