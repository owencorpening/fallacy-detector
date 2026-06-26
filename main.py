#!/usr/bin/env python3
import argparse
import os
import sys
import yaml


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def resolve_env(value: str) -> str:
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        var = value[2:-1]
        resolved = os.environ.get(var)
        if not resolved:
            print(f"Error: environment variable {var} is not set", file=sys.stderr)
            sys.exit(1)
        return resolved
    return value


def build_stt(cfg: dict):
    provider = cfg.get("provider", "whisper-local")
    if provider == "whisper-local":
        from adapters.stt.whisper_local import WhisperLocalAdapter
        return WhisperLocalAdapter(model_size=cfg.get("model_size", "tiny"))
    elif provider == "openai-whisper":
        from adapters.stt.openai_whisper import OpenAIWhisperAdapter
        return OpenAIWhisperAdapter(
            api_key=resolve_env(cfg["api_key"]),
            model=cfg.get("model", "whisper-1"),
        )
    else:
        print(f"Unknown STT provider: {provider}", file=sys.stderr)
        sys.exit(1)


def build_llm(cfg: dict):
    provider = cfg.get("provider", "anthropic")
    if provider == "anthropic":
        from adapters.llm.anthropic_adapter import AnthropicAdapter
        return AnthropicAdapter(
            api_key=resolve_env(cfg.get("api_key", "${ANTHROPIC_API_KEY}")),
            model=cfg.get("model", "claude-haiku-4-5-20251001"),
        )
    elif provider == "openai":
        from adapters.llm.openai_adapter import OpenAIAdapter
        return OpenAIAdapter(
            api_key=resolve_env(cfg["api_key"]),
            model=cfg.get("model", "gpt-4o-mini"),
        )
    else:
        print(f"Unknown LLM provider: {provider}", file=sys.stderr)
        sys.exit(1)


def build_source(args, pipeline_cfg: dict):
    sample_rate = pipeline_cfg.get("sample_rate", 16000)
    chunk_seconds = pipeline_cfg.get("chunk_seconds", 5)

    source = args.source or "mic"

    if source == "file":
        if not args.file:
            print("Error: --file required with --source file", file=sys.stderr)
            sys.exit(1)
        from transport.file import FileAudioSource
        return FileAudioSource(args.file, chunk_seconds=chunk_seconds, sample_rate=sample_rate)
    elif source == "stream":
        if not args.url:
            print("Error: --url required with --source stream", file=sys.stderr)
            sys.exit(1)
        from transport.stream_url import StreamURLAudioSource
        return StreamURLAudioSource(args.url, chunk_seconds=chunk_seconds, sample_rate=sample_rate)
    elif source == "youtube":
        if not args.url:
            print("Error: --url required with --source youtube", file=sys.stderr)
            sys.exit(1)
        from transport.youtube import YouTubeAudioSource
        return YouTubeAudioSource(args.url, chunk_seconds=chunk_seconds, sample_rate=sample_rate)
    elif source == "mic":
        from transport.microphone import MicrophoneAudioSource
        return MicrophoneAudioSource(chunk_seconds=chunk_seconds, sample_rate=sample_rate)
    else:
        print(f"Unknown source: {source}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Real-time logical fallacy detector")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--source", choices=["file", "stream", "youtube", "mic"], default="mic")
    parser.add_argument("--file", help="Path to audio file (with --source file)")
    parser.add_argument("--url", help="URL for --source stream or youtube")
    args = parser.parse_args()

    config = load_config(args.config)
    pipeline_cfg = config.get("pipeline", {})

    stt = build_stt(config.get("stt", {}))
    llm = build_llm(config.get("llm", {}))
    source = build_source(args, pipeline_cfg)

    from core.pipeline import Pipeline
    pipeline = Pipeline(
        source=source,
        stt=stt,
        llm=llm,
        context_window=pipeline_cfg.get("context_window", 3),
    )

    try:
        pipeline.run()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
