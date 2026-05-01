import os
from pathlib import Path

def write_file(working_directory=".", file_path=None, content=None):
    path_wd = Path(working_directory).resolve()
    path_d = Path(working_directory, file_path).resolve()

    if not path_d.startswith(path_wd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(path_d):
        newdir = os.path.dirname(path_d)
        
        try:
            os.makedirs(newdir, exist_ok=True)
        except Exception as e:
            return f"Error creating dirs- '{newdir}': {e}"
        
    try:
        with open(path_d, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing to file '{file_path}': {e}"
