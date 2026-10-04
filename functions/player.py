# This file is a specific terminal function for playing songs.

import subprocess

mpv_process = None

def player(SONG):
    global mpv_process
    """To Play a specified song.

    ARGS:
        SONG: The song to play"""

#    if mpv_process is not None:
    subprocess.run(["pkill", "mpv"])
    
    query = f"ytsearch1:{SONG}"
    song = subprocess.check_output([
        "yt-dlp", "--impersonate", "chrome",
        "-f", "bestaudio",
        "-g",
        query,
    ])

    play = subprocess.Popen(["mpv", song])
    return f"Now playing: {SONG}"

if __name__ == "__main__":
    player("Eye for an Eye John Wick")