from collections.abc import Iterator
import av
import numpy as np

from transport.base import AudioSource

# av.open handles HTTP, RTSP, and HLS transparently via ffmpeg.
# For RTSP: rtsp://host/path
# For HLS:  http://host/playlist.m3u8
# For HTTP MP3/AAC: http://host/stream.mp3


class StreamURLAudioSource(AudioSource):
    def __init__(self, url: str, chunk_seconds: float = 5.0, sample_rate: int = 16000):
        self._url = url
        self._chunk_size = int(chunk_seconds * sample_rate)
        self._sample_rate = sample_rate

    def chunks(self) -> Iterator[np.ndarray]:
        options = {
            "rtsp_transport": "tcp",   # more reliable than UDP for RTSP
            "stimeout": "5000000",     # 5s connection timeout (microseconds)
        }
        container = av.open(self._url, options=options)
        resampler = av.AudioResampler(format="fltp", layout="mono", rate=self._sample_rate)

        buf: list[np.ndarray] = []
        buf_len = 0

        def _drain(frame) -> Iterator[np.ndarray]:
            nonlocal buf, buf_len
            for rf in resampler.resample(frame):
                arr = rf.to_ndarray()[0]
                buf.append(arr)
                buf_len += len(arr)
                while buf_len >= self._chunk_size:
                    combined = np.concatenate(buf)
                    yield combined[: self._chunk_size]
                    remainder = combined[self._chunk_size :]
                    buf = [remainder] if len(remainder) else []
                    buf_len = len(remainder)

        try:
            for frame in container.decode(audio=0):
                yield from _drain(frame)
        finally:
            container.close()
