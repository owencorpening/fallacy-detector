from collections.abc import Iterator
import av
import numpy as np

from transport.base import AudioSource


class FileAudioSource(AudioSource):
    def __init__(self, path: str, chunk_seconds: float = 5.0, sample_rate: int = 16000):
        self._path = path
        self._chunk_size = int(chunk_seconds * sample_rate)
        self._sample_rate = sample_rate

    def chunks(self) -> Iterator[np.ndarray]:
        container = av.open(self._path)
        resampler = av.AudioResampler(format="fltp", layout="mono", rate=self._sample_rate)

        buf: list[np.ndarray] = []
        buf_len = 0

        def _drain(frame) -> Iterator[np.ndarray]:
            nonlocal buf, buf_len
            for rf in resampler.resample(frame):
                arr = rf.to_ndarray()[0]  # (n_samples,) float32
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
            # flush resampler
            yield from _drain(None)
        finally:
            container.close()

        # yield final partial chunk if any audio remains
        if buf:
            combined = np.concatenate(buf)
            if len(combined):
                yield combined
