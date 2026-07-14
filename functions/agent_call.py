import os
import time
from dotenv import load_dotenv
from functions.tool import tools
from groq import Groq, RateLimitError

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


def agent_call(messages):
    max_attempts = 5
    for attempt in range(max_attempts): # attempt = 0, 1, 2,...
        try:
            response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages,
                    tools=tools,
                    temperature=0.0,  # Keep temperature between 0.0 - 0.5 for best tool calling results
                    tool_choice="auto",
                    max_completion_tokens=4096,
                )
            return response
        
        except RateLimitError as e:
            if attempt == max_attempts - 1:
                raise
            wait = getattr(e, "retry_after", None) or 15
            print(f"Rate Limit Error, retrying in {wait}s (attempt {attempt+1} / {max_attempts})")
            time.sleep(wait)


def final_call(messages):
    response = client.chat.completions.create(  # We don't need the tools during response because it will always try to
            model="openai/gpt-oss-120b",       #  use tools, which we don't want after tool use
            messages=messages,
        )
    
    return response

