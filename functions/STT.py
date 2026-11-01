import os
import time
import webrtcvad
import numpy as np
from groq import Groq
from dotenv import load_dotenv
from scipy.io.wavfile import write


vad = webrtcvad.Vad(3) # aggressiveness 0-3 

silence_limit = 50


def STT(audio_input):
    while not audio_input.STT_queue.empty():
        audio_input.STT_queue.get_nowait()
    
    frames = []
    silence_counter = 0

    audio_input.STT_active.set()

    print("Recording...")

    try:
        while silence_counter < silence_limit:
            audio_frame = audio_input.STT_queue.get()
            frames.append(audio_frame)

            chunks = np.split(audio_frame, 4)

            for chunk in chunks:
                audio = chunk.tobytes()
                
                try:
                    is_speech = vad.is_speech(audio, 16000)
                except Exception:
                    is_speech = False
                
                if is_speech:
                    silence_counter = 0
                else:
                    silence_counter += 1

                if silence_counter >= silence_limit:
                    break


        recorded = np.concatenate(frames, axis=0)

        write("output.wav", 16000, recorded)

        load_dotenv()
        API_KEY = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=API_KEY)

        with open("output.wav", "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", file.read()),
                model="whisper-large-v3-turbo",
            )

        prompt = transcription.text
        print(prompt)
        return prompt

    finally:
        audio_input.STT_active.clear()

