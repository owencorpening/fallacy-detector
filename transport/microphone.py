# Requires audio hardware + sounddevice + PortAudio.
import collections
import queue
from collections.abc import Iterator
import numpy as np
import sounddevice as sd

from transport.base import AudioSource


class MicrophoneAudioSource(AudioSource):
    def __init__(self, chunk_seconds: float = 5.0, sample_rate: int = 16000):
        self._chunk_size = int(chunk_seconds * sample_rate)
        self._sample_rate = sample_rate
        self._queue: queue.Queue[np.ndarray] = queue.Queue()

    def _callback(self, indata: np.ndarray, frames: int, time, status) -> None:
        self._queue.put(indata.copy())

    def chunks(self) -> Iterator[np.ndarray]:
        buf: list[np.ndarray] = []
        buf_len = 0

        with sd.InputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype="float32",
            callback=self._callback,
            blocksize=1024,
        ):
            print(f"Listening via microphone... (press Ctrl+C to stop)")
            while True:
                block = self._queue.get()
                buf.append(block)
                buf_len += len(block)

                if buf_len >= self._chunk_size:
                    audio = np.concatenate(buf).flatten()
                    buf = []
                    buf_len = 0
                    yield audio
