import sounddevice as sd
from queue import Queue


sr=16000
frame_duration = 80
frame_size = int(sr * frame_duration / 1000)
frames = Queue()
Threshold = 0.8


class SoundDevice():
    def __init__(self):
        self.stream = None

    def callback(indata, frames_count, time_info, status):
        frames.put(indata.copy().flatten())

    def InputStream(self):
        self.stream = sd.InputStream(
            samplerate=sr,
            blocksize=frame_size,
            channels=1,
            dtype='int16',
            callback=self.callback,
        )

