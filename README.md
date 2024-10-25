# TwitchPlays
These files allows Twitch Chat or Youtube Chat to control your keyboard or mouse to play a game.

This is an extended version of [DougDoung's Twitch plays scripts](https://github.com/DougDougGithub/TwitchPlays). Cleaned up and made more Pythonic


# Installing
Download and Extract the files from [Here](https://github.com/DaBloodyResh/TwitchPlays/archive/refs/heads/main.zip)

To run the code you will need to install Python 3.9 or newer.  
If you don't have python installed already, and you are running Windows, get it [from here](https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe) **and be sure to click "Add Python to environment variables"** in the installer (Under Customize Install -> Advanced Options)

Additionally, you will need to install the following python modules using Pip:

```bash
pip install -r  requirements.txt
```

Once Python is set up, simply change the Twitch username (or Youtube channel ID) in TwitchPlays_TEMPLATE.py, and you'll be ready to go.

# Example Useage
```py
from TwitchPlays_CommandManager import CommandManager as exe
from TwitchPlays_KeyCodes import Key, HoldAndReleaseKey

# Move left for 2s
@exe.command("left")
def move_left():
    HoldAndReleaseKey(Key.A, 2)

# Start it running
if __name__ == "__main__":
    manager = run('TwitchUserName')
    manager.countdown()
    manager.process_messages()
```

# Credit
This code is originally based off Wituz's Twitch Plays template, then expanded by DougDoug and DDarknut with help from Ottomated for the Youtube side. Modifications and clean up by catboy. 
