import os
from groq import Groq
from functions.tool import tools

api_key = os.getenv("GROK_API_KEY")
client = Groq(api_key=api_key)


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


