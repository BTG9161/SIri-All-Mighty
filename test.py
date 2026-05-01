import threading
import keyboard
from dotenv import load_dotenv
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import requests
import sys

load_dotenv()
eleven_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

API_KEY=os.getenv("ELEVENLABS_API_KEY")
samplerate = 16000

buffer = ""
lock = threading.Lock()

def transcribe(filename):
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {"xi-api-key": API_KEY}

    with open(filename, "rb") as f:
        response = requests.post(
            url,
            headers=headers,
            files={"file": f}
        )

    return response.json()["text"]

def speech_thread():
    global buffer

    while True:
        keyboard.wait("space")

        recording = []

        def callback(indata, frames, time, status):
            recording.append(indata.copy())

        stream = sd.InputStream(
            samplerate=samplerate,
            channels=1,
            dtype="int16",
            callback=callback
        )

        stream.start()
        print("\nListening...")

        keyboard.wait("space", trigger_on_release=True)

        stream.stop()
        stream.close()

        audio = np.concatenate(recording, axis=0)
        wav.write("input.wav", samplerate, audio)

        print("Transcribing...")
        text = transcribe("input.wav")

        with lock:
            buffer += " " + text

        # print without killing the input prompt too badly
        sys.stdout.write(f"\n[SPEECH]: {text}\n")
        sys.stdout.flush()

# Start speech listener
threading.Thread(target=speech_thread, daemon=True).start()

# Main typing loop
while True:
    typed = input("> ")

    with lock:
        buffer += " " + typed
        print("[BUFFER]:", buffer)
