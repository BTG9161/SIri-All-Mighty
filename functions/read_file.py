import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
DIR = os.getenv("DIR")

def read_file(file_path: str, working_directory = DIR) -> str:
    """Read a file on the user's system.
    
    ARGS:
        file_path: The path relative to the working directory.
        working_directory: The working directory of the file, you don't need to specify it unless stated otherwise."""
    wd = Path(working_directory).resolve()
    file = Path(wd, file_path).resolve()

    if not os.path.exists(file):
        return f"File doesn't exist, apparently"

    try:
        with open(file, 'r') as f:
            contents = f.read()

            return contents

    except Exception as e:
        return f" Error reading file '{file_path}': {e}"

