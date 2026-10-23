import os
from pathlib import Path
from dotenv import load_dotenv
from functions.memory import memory_access

load_dotenv()
DIR = os.getenv("DIR")

files = [".config/SOUL.md", ".config/USER.md", "system_prompt.txt"]
parts = []

def build_system_prompt():
    for file in files:
        path_to_file = Path(DIR, file)
        parts.append(path_to_file.read_text(encoding="utf-8"))

    memories = memory_access()
    if memories:
        parts.append("Long-term memories: \n" + memories)

    return "\n\n".join(parts)

