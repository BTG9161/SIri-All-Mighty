import os
from mem0 import Memory
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {"path": "/Users/bhupatejassingh/Siri/.venv/lib/python3.12/site-packages/chromadb"}
    },
    "llm": {
        "provider": "groq",   # you're already using Groq for Whisper — can reuse for extraction
        "config": {
            "model": "openai/gpt-oss-20b",
            "api_key": GROQ_API_KEY
        }
    },
    "embedder": {
    "provider": "fastembed",
    "config": {
        "model": "BAAI/bge-small-en-v1.5",
        "embedding_dims": 384
        }
    }
}



m = Memory.from_config(config)

memory = Memory.from_config(config)

messages = [
    {"role": "user", "content": "I'm Bhupat and I'm building a drone."},
    {"role": "assistant", "content": "I'll remember that."}
]

memory.add(messages, user_id="bhupat")

results = memory.search(
    "What project is the user working on?",
    user_id="bhupat"
)

print(results)

