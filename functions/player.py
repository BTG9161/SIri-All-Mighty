# This file is a specific terminal function for playing songs.

import signal
import subprocess


class Player:
    """This class is used for handling songs using yt-dlp and mpv.
    """
    def __init__(self):
        self.mpv = None
    
    def play(self, SONG):
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

        self.mpv = subprocess.Popen([
            "mpv",
            "--no-terminal",
            song
            ],
        )
        
        return f"Now playing: {SONG}"

    def pause(self):
            """To pause the current song.
            ARGS:
                None"""
    
            if self.mpv is not None:
                self.mpv.send_signal(signal.SIGSTOP)
    
            return "Song paused playing the song."
    
    def resume(self):
            """To resume the current song.
            ARGS:
                None"""
    
            if self.mpv is not None:
                self.mpv.send_signal(signal.SIGCONT)
    
            return "Song resumed playing the song."
    

if __name__ == "__main__":
    player = Player()
    player.play("Eye for an Eye John Wick")

    x = input("Press Enter to stop playing the song...")
    if x == "s":
        player.stop()

