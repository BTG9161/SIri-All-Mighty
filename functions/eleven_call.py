import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv


# Load environment variables (API keys, etc.)
load_dotenv()

# Initialize ElevenLabs TTS client
eleven_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

def eleven_call(reply):
    try:
        audio = eleven_client.text_to_speech.convert(
            text     = reply,
            voice_id = "pFZP5JQG7iQjIQuC4Bku",
            model_id = "eleven_multilingual_v2",
            )

            # Save audio file
        save(audio, "output.mp3")
    
    except Exception as e:
        return f"Error {e} occured"

