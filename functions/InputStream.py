import sounddevice as sd
from threading import Event
from queue import Queue, Empty, Full


sr=16000
frame_duration = 80
frame_size = int(sr * frame_duration / 1000)
Threshold = 0.8


class SoundDevice():
    def __init__(self):
        self.stream = None
        self.STT_active = Event()
        self.wake_queue = Queue(maxsize=20)
        self.STT_queue = Queue(maxsize=100)

    def distribute(self, queue, frame):
        try:
            queue.put_nowait(frame.copy())
        except Full:
            try:
                queue.get_nowait()
            except Empty:
                pass

            queue.put_nowait(frame.copy())

    def callback(self, indata, frames_count, time_info, status):
        frame = indata.copy().flatten()

        self.distribute(self.wake_queue, frame)

        if self.STT_active.is_set():
            self.distribute(self.STT_queue, frame)

    def start(self):
        self.stream = sd.InputStream(
            samplerate=sr,
            blocksize=frame_size,
            channels=1,
            dtype='int16',
            callback=self.callback,
        )

        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

