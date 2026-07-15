import os
from datetime import datetime, date
from pathlib import Path


today = datetime.today()

def store_session(session):
    """
    This functions is used to store sessions.
    ARGS:
        session: This is the current sessions that needs to be stored."""
    
    cur_session_path = Path(session)
    session_path = Path(f"/Users/bhupatejassingh/Siri/sessions/{today.day}-{today.month}-{today.year} {today.hour}:{today.minute}:{today.second}").resolve()

    if not session_path.exists():
        session_dir = Path(os.path.dirname(session_path))

        try:
            os.makedirs(session_dir, exist_ok=True)
        except Exception as e:
            return f"Error creating dirs- '{session_dir}': {e}"
        
    
    with session_path.open('w', encoding="utf-8") as file:
        with cur_session_path.open('r') as session_file:
            file.write(session_file.read())

def del_sessinon():
    pass

if __name__ == "__main__":
    store_session("/Users/bhupatejassingh/Siri/current_session.json")

