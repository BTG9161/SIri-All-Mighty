import shutil
from datetime import datetime
from pathlib import Path

SESSIONS_DIR = Path("/Users/bhupatejassingh/Siri/sessions")

today = datetime.today()


def session_storage(current_session_path):
    current_session_path = Path(current_session_path)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    dest_path = SESSIONS_DIR / f"{today.day}-{today.month}-{today.year}.json"

    if not current_session_path.exists():
        print(f"No current session file found at {current_session_path}, nothing to archive.")
        return

    shutil.copy(current_session_path, dest_path)
    print(f"Archived session to {dest_path}")


if __name__ == "__main__":
    session_storage("/Users/bhupatejassingh/Siri/current-session.json")
