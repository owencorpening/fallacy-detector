import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from transport.youtube import _resolve_audio_url, YouTubeAudioSource
from transport.stream_url import StreamURLAudioSource


def make_ydl_mock(resolved_url: str):
    mock_instance = MagicMock()
    mock_instance.extract_info.return_value = {"url": resolved_url}
    mock_cm = MagicMock()
    mock_cm.__enter__.return_value = mock_instance
    mock_cm.__exit__.return_value = False
    return mock_cm, mock_instance


def test_resolve_returns_extracted_url():
    mock_cm, mock_instance = make_ydl_mock("https://cdn.example.com/audio.webm")
    with patch("yt_dlp.YoutubeDL", return_value=mock_cm):
        url = _resolve_audio_url("https://youtube.com/watch?v=abc123")
    assert url == "https://cdn.example.com/audio.webm"


def test_resolve_calls_extract_info_with_no_download():
    mock_cm, mock_instance = make_ydl_mock("https://cdn.example.com/audio.webm")
    with patch("yt_dlp.YoutubeDL", return_value=mock_cm):
        _resolve_audio_url("https://youtube.com/watch?v=abc123")
    mock_instance.extract_info.assert_called_once_with(
        "https://youtube.com/watch?v=abc123", download=False
    )


def test_youtube_source_is_stream_url_source():
    with patch("transport.youtube._resolve_audio_url", return_value="https://cdn.example.com/audio.webm"):
        source = YouTubeAudioSource("https://youtube.com/watch?v=abc123")
    assert isinstance(source, StreamURLAudioSource)


def test_youtube_source_passes_chunk_seconds():
    with patch("transport.youtube._resolve_audio_url", return_value="https://cdn.example.com/audio.webm"):
        source = YouTubeAudioSource("https://youtube.com/watch?v=abc123", chunk_seconds=10)
    assert source._chunk_size == 10 * 16000


def test_ydl_uses_bestaudio_format():
    mock_cm, _ = make_ydl_mock("https://cdn.example.com/audio.webm")
    with patch("yt_dlp.YoutubeDL", return_value=mock_cm) as MockYDL:
        _resolve_audio_url("https://youtube.com/watch?v=abc123")
    opts = MockYDL.call_args[0][0]
    assert opts["format"] == "bestaudio/best"
    assert opts["quiet"] is True
