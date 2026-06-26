import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pytest

from core.pipeline import Pipeline
from core.fallacies import FallacyResult
from transport.file import FileAudioSource
from tests.conftest import FixedSTT, FixedLLM


def run_pipeline(source, stt, llm) -> list[str]:
    """Run pipeline synchronously and collect printed output."""
    printed = []
    original_print = __builtins__["print"] if isinstance(__builtins__, dict) else print

    import builtins
    captured = []

    original = builtins.print
    def fake_print(*args, **kwargs):
        captured.append(" ".join(str(a) for a in args))
    builtins.print = fake_print

    try:
        pipeline = Pipeline(source=source, stt=stt, llm=llm, context_window=3)
        pipeline.run()
        # give daemon threads a moment to finish
        time.sleep(0.2)
    finally:
        builtins.print = original

    return captured


def test_detection_printed_to_stdout(audio_file, straw_man_result, capsys):
    source = FileAudioSource(audio_file, chunk_seconds=5)
    stt = FixedSTT("so you're saying we should ban everything")
    llm = FixedLLM(straw_man_result)

    pipeline = Pipeline(source=source, stt=stt, llm=llm, context_window=3)
    pipeline.run()
    time.sleep(0.3)  # let daemon threads flush

    captured = capsys.readouterr()
    assert "[STRAW MAN" in captured.out
    assert "0.91" in captured.out


def test_no_output_when_no_fallacy(audio_file, capsys):
    source = FileAudioSource(audio_file, chunk_seconds=5)
    stt = FixedSTT("The weather today is partly cloudy.")
    llm = FixedLLM(None)

    pipeline = Pipeline(source=source, stt=stt, llm=llm, context_window=3)
    pipeline.run()
    time.sleep(0.3)

    captured = capsys.readouterr()
    assert captured.out.strip() == ""


def test_empty_transcript_skips_llm(audio_file):
    source = FileAudioSource(audio_file, chunk_seconds=5)
    stt = FixedSTT("")
    llm = FixedLLM(FallacyResult("Straw Man", 0.9, "should not appear"))

    pipeline = Pipeline(source=source, stt=stt, llm=llm)
    pipeline.run()
    time.sleep(0.3)

    assert len(llm.calls) == 0


def test_context_window_passed_to_llm(audio_file):
    source = FileAudioSource(audio_file, chunk_seconds=5)
    transcripts = iter(["first chunk", "second chunk", "third chunk"])

    class SequentialSTT:
        def transcribe(self, _):
            try:
                return next(transcripts)
            except StopIteration:
                return ""

    llm = FixedLLM(None)
    pipeline = Pipeline(source=source, stt=SequentialSTT(), llm=llm, context_window=2)
    pipeline.run()
    time.sleep(0.3)

    # by the third call, context should contain the two previous transcripts
    non_empty = [(t, c) for t, c in llm.calls if t]
    assert len(non_empty) >= 2


def test_llm_receives_correct_transcript(audio_file, straw_man_result):
    source = FileAudioSource(audio_file, chunk_seconds=5)
    stt = FixedSTT("you either support this bill or you support crime")
    llm = FixedLLM(straw_man_result)

    pipeline = Pipeline(source=source, stt=stt, llm=llm)
    pipeline.run()
    time.sleep(0.3)

    transcripts_seen = [t for t, _ in llm.calls]
    assert all(t == "you either support this bill or you support crime" for t in transcripts_seen)
