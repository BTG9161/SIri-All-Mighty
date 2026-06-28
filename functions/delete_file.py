import os
from pathlib import Path


def delete_file(file_path, working_directory="/Users/bhupatejassingh/Siri") -> str:
    """To delete the specified file.
    ARGS:
        file_path: The file path relative to the working directory.
        working_directory: The working directory of the file, you don't need to specify it unless stated otherwise."""
    path_wd = Path(working_directory).resolve()
    path_file = Path(working_directory, file_path).resolve()

    if path_wd not in path_file.parents and path_file != path_wd:
        return f"Error deleting file {path_file}, as it is outside the permitted working directory."
    
    try:
        os.remove(path_file)
    
    except Exception as e:
        return f"{e} occured durin delting file {path_file}"

    return f"{file_path} deleted successfully."



