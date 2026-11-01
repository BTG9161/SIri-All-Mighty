from queue import Queue
from openwakeword.model import Model
from functions.InputStream import SoundDevice


sd = SoundDevice()

model = Model(
    wakeword_model_paths=["/home/btg/Siri/.venv/lib/python3.12/site-packages/openwakeword/resources/models/alexa_v0.1.onnx"]
)


class WakeWord():
    def __init__(self, audio_input):
        self.audio_input = audio_input
        self.wake_done = False
        self.wake_received = False

    def passive_wakeword_detection(self): # This will be in a thread in siriApp        
        try:
            while True:
                if self.wake_received:
                    self.wake_done = False
                    self.wake_received = False

                audio_frame = self.audio_input.wake_queue.get()

                predictions = model.predict(audio_frame)

                for _, score in predictions.items():
                    if score > 0.8:
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

