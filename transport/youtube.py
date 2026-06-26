import yt_dlp
from transport.stream_url import StreamURLAudioSource


def _resolve_audio_url(url: str) -> str:
    opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


class YouTubeAudioSource(StreamURLAudioSource):
    def __init__(self, url: str, chunk_seconds: float = 5.0, sample_rate: int = 16000):
        stream_url = _resolve_audio_url(url)
        super().__init__(stream_url, chunk_seconds=chunk_seconds, sample_rate=sample_rate)
