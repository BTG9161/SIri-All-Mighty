import os
from pathlib import Path


def delete_file(working_directory=".", file_path=None ):
    path_wd = Path(working_directory).resolve()
    path_file = Path(working_directory, file_path).resolve()

    if path_wd not in path_file.parents and path_file != path_wd:
        return f"Error deleting file {path_file}, as it is outside the permitted working directory."
    
    try:
        os.remove(path_file)
    
    except Exception as e:
        return f"{Exception} occured durin delting file {path_file}"

    return f"{file_path} deleted successfully."



