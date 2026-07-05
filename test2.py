import os
from dotenv import load_dotenv
from groq import Groq
from pynput import keyboard
import webrtcvad
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time

# Track currently pressed keys
current = set()

vad = webrtcvad.Vad(2)

wake = {keyboard.Key.ctrl, keyboard.Key.shift}

def on_press(key):
    current.add(key)
    if all(k in current for k in wake):
        print('Pressed...')

def on_release(key):
    if key in current:
        current.discard(key)
    
    if key == wake:
        listener.stop()

sr = 32000 #Sample Rate, webrtcvad requires 8000, 16000, 32000, or 48000 Hz
frame_duration = 30 # in ms, must be 10, 20, or 30
frame_size = int(sr * frame_duration/1000)

frames=[] #All the frames of the recording.
silence_limit = 50 # 1 frame is 30ms, and if silence for 50 frames => 1.5s of silence
silence_counter = 0
recording_done = False


def callback(indata, frame_count, time_info, status):   #callback is the function which sd calls after it attains a certain chunk of data, and the args of callback are obv constant.
    global silence_counter, recording_done
    
    frames.append(indata.copy())

    audio_bytes = indata.tobytes()
    is_speech = vad.is_speech(audio_bytes, sr) # it needs st because it cannot tell with one pressure wave per chunk that what is happening, and also without time it cannot tell the freq of the sound
    
    if is_speech:
        silence_counter = 0
    else:
        silence_counter += 1
    
    if silence_counter>silence_limit:
        recording_done = True
    

stream = sd.InputStream(samplerate=sr,
                        channels=1,
                        blocksize=frame_size,
                        dtype='int16',
                        callback=callback,
                        )

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

    stream.start()
    while not recording_done:
        time.sleep(0.5)
    print('Recording...')

    if not recording_done:
        recording = np.concatenate(frames, axis=0)
    else:
        stream.close()
        stream.stop()

    write("output.wav", sr, recording)
    print("Saved to output.wav")

    load_dotenv()
    API_KEY = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=API_KEY)

    with open("output.wav", "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", file.read()),
            model="whisper-large-v3-turbo",
        )

    print(transcription.text)

