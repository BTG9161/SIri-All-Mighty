import sounddevice
import numpy as np
from queue import Queue
from openwakeword.model import Model


sr=16000
frame_duration = 80
frame_size = int(sr * frame_duration / 1000)
frames = Queue()
Threshold = 0.8

model = Model(
    wakeword_model_paths=["/home/btg/Siri/.venv/lib/python3.12/site-packages/openwakeword/resources/models/alexa_v0.1.onnx"]
)

def callback(indata, frames_count, time_info, status):
    frames.put(indata.copy().flatten())


class WakeWord():
    def __init__(self):
        self.wake_done = False
        self.wake_received = False

    def passive_wakeword_detection(self): # This will be in a thread in siriApp        
        try:        
            with sounddevice.InputStream(
                samplerate=sr,
                blocksize=frame_size,
                channels=1,
                dtype='int16',
                callback=callback
            ):
                while True:
                    if self.wake_received:
                        self.wake_done = False
                        self.wake_received = False

                    audio_frame = frames.get()

                    predictions = model.predict(audio_frame)

                    for _, score in predictions.items():
                        if score > Threshold:
                            self.wake_done = True
                            break

        except Exception as e:
            self.wake_done = False
            return f"ERROR: {e}"


if __name__ == "__main__":
    import time
    import threading

    wakeword = WakeWord()
    wakeword_detection = threading.Thread(target=wakeword.passive_wakeword_detection)

    wakeword_detection.start()


    while True:
        if wakeword.wake_done:
            print(True)
            wakeword.wake_done = False
        else:
            print(False)

        time.sleep(0.5)

