import os
from dotenv import load_dotenv
from groq import Groq
from functions.tool import tools

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


def agent_call(messages):
    response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            temperature=0.0,  # Keep temperature between 0.0 - 0.5 for best tool calling results
            tool_choice="auto",
            max_completion_tokens=4096,
        )
    return response

def final_call(messages):
    response = client.chat.completions.create(  # We don't need the tools during response because it will always try to
            model="llama-3.1-8b-instant",       #  use tools, which we don't want after tool use
            messages=messages,
        )
    
    return response


