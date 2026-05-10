import os
from groq import Groq
from dotenv import load_dotenv 




api_key = os.getenv("GROK_API_KEY")
client = Groq(api_key=api_key)


def agent_call(messages):
    response = client.chat.completions.create(     #response
        model="llama-3.1-8b-instant",
        messages=messages
    )

    return response

