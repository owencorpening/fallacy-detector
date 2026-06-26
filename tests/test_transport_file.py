import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from transport.file import FileAudioSource

SAMPLE_RATE = 16000
CHUNK_SECONDS = 5


def test_yields_correct_chunk_size(audio_file):
    source = FileAudioSource(audio_file, chunk_seconds=CHUNK_SECONDS, sample_rate=SAMPLE_RATE)
    chunks = list(source.chunks())

    # 12s audio / 5s chunks = 2 full chunks + 1 partial
    assert len(chunks) == 3
    assert len(chunks[0]) == CHUNK_SECONDS * SAMPLE_RATE
    assert len(chunks[1]) == CHUNK_SECONDS * SAMPLE_RATE
    assert len(chunks[2]) < CHUNK_SECONDS * SAMPLE_RATE  # partial tail


def test_chunks_are_float32(audio_file):
    source = FileAudioSource(audio_file, chunk_seconds=CHUNK_SECONDS, sample_rate=SAMPLE_RATE)
    for chunk in source.chunks():
        assert chunk.dtype == np.float32


def test_short_file_yields_single_partial_chunk(short_audio_file):
    source = FileAudioSource(short_audio_file, chunk_seconds=CHUNK_SECONDS, sample_rate=SAMPLE_RATE)
    chunks = list(source.chunks())
    # 3s < 5s chunk, so one partial chunk
    assert len(chunks) == 1
    assert len(chunks[0]) < CHUNK_SECONDS * SAMPLE_RATE


def test_chunk_seconds_respected(audio_file):
    source = FileAudioSource(audio_file, chunk_seconds=3, sample_rate=SAMPLE_RATE)
    chunks = list(source.chunks())
    full_chunks = [c for c in chunks[:-1]]
    for c in full_chunks:
        assert len(c) == 3 * SAMPLE_RATE


def test_total_samples_preserved(audio_file):
    source = FileAudioSource(audio_file, chunk_seconds=CHUNK_SECONDS, sample_rate=SAMPLE_RATE)
    chunks = list(source.chunks())
    total = sum(len(c) for c in chunks)
    # 12s * 16000 = 192000 samples (allow small resampler rounding)
    assert abs(total - 12 * SAMPLE_RATE) < 512
