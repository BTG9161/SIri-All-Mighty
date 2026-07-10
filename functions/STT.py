from .wake import wake_done, input_queue
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time
import os
from dotenv import load_dotenv
from groq import Groq
import webrtcvad

vad = webrtcvad.Vad(2) # aggressiveness 0-3 

recording = False
sr=32000
frame_duration = 30
frame_size = int(sr * frame_duration / 1000)
frames=[]
silence_counter = 0
silence_limit = 50


def callback(indata, frame_count, time_info, status):
    global recording, silence_counter
    frames.append(indata.copy())

    audio = indata.tobytes()
    
    try:
        is_speech = vad.is_speech(audio, sr)
    except Exception:
        is_speech = False
    
    if is_speech:
        silence_counter = 0
    else:
        silence_counter += 1
    
    if silence_counter > silence_limit:
        recording = False
    

def STT():
    global recording, silence_counter, frames, prompt, listener

    recording = False
    silence_counter = 0
    frames = []
    
    wake_done.wait()
    recording = True
    wake_done.clear()

    stream = sd.InputStream(samplerate=sr,
                            blocksize=frame_size,
                            channels=1,
                            dtype='int16',
                            callback=callback
                            )

    try:
        stream.start()
        print('Recording...')

        while recording:
            time.sleep(0.5)

        stream.stop()
        stream.close()
    
    except Exception:
        pass

    recorded = np.concatenate(frames, axis=0)

    write("output.wav", sr, recorded)
    print("Saved to output.wav")

    load_dotenv()
    API_KEY = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=API_KEY)

    with open("output.wav", "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", file.read()),
            model="whisper-large-v3-turbo",
        )

    prompt = transcription.text
    input_queue.put(prompt)
    print(prompt)
    return prompt

def STT_loop():
    while True:
        STT()

