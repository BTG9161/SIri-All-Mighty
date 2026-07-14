import os
from pathlib import Path

def write_file(working_directory="", file_path=None, content=None) -> str:
    """Write to a file on the user's system.
    
    ARGS:
        working_directory: The working directory of the file, you don't need to specify it unless stated otherwise.
        file_path: The path relative to the working directory.
        content: The content of the file."""
    path_wd = Path(working_directory).resolve()
    path_d = Path(working_directory, file_path).resolve()

    if path_wd not in path_d.parents and path_d != path_wd:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(path_d):
        newdir = os.path.dirname(path_d)
        
        try:
            os.makedirs(newdir, exist_ok=True)
        except Exception as e:
            return f"Error creating dirs- '{newdir}': {e}"
        
    try:
        with open(path_d, 'w', encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing to file '{file_path}': {e}"
