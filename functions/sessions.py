import os
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from .delete_file import delete_file

load_dotenv()

DIR = os.getenv("DIR")
SESSIONS = Path(DIR, "sessions").resolve()
today = datetime.today()

def store_session(session):
    """
    This functions is used to store sessions.
    ARGS:
        session: This is the current sessions that needs to be stored.
    """
    
    cur_session_path = Path(session)
    session_path = Path(f"{SESSIONS}/{today.day}-{today.month}-{today.year} {today.hour}:{today.minute}:{today.second}").resolve()

    if not session_path.exists():
        session_dir = Path(os.path.dirname(session_path))

        try:
            os.makedirs(session_dir, exist_ok=True)
        except Exception as e:
            return f"Error creating dirs- '{session_dir}': {e}"
        
    
    with session_path.open('w', encoding="utf-8") as file:
        with cur_session_path.open('r') as session_file:
            file.write(session_file.read())

    os.remove("current_session.json")


def del_session(session_file):
    """
    This function is used to delete session files, which the user asks.
    ARGS:
        session_file: This is the session_file the user asks to delete.
    """
    delete_file(session_file, SESSIONS)


if __name__ == "__main__":
    x=del_session("22-7-2026 17:35:21")
    print(x)

