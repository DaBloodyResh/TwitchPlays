# TwitchPlays
These files allows Twitch Chat or Youtube Chat to control your keyboard or mouse to play a game.


Original code is [DougDoung's Twitch plays scripts](https://github.com/DougDougGithub/TwitchPlays). Me (Wyatt) replaced a lot of code and restructured most of it to match with the already used pyautogui syntax, and added a gui window for ease of access to creating a new command.


# Installing
Download and Extract the files from [Here](https://github.com/DaBloodyResh/TwitchPlays/archive/refs/heads/main.zip)

To run the code you will need to install Python 3.11 or newer.  
If you don't have python installed already, and you are running Windows, get it [from here]([https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe](https://www.python.org/downloads/release/python-3110/)) **and be sure to click "Add Python to environment variables"** in the installer (Under Customize Install -> Advanced Options)

Additionally, you will need to install the following python modules using Pip:

```bash
pip install -r  requirements.txt
pip install keyboard
pip install pyautogui
pip install PySimpleGUI
```

PySimpleGUI is used for the PyUI.py file for the UI window, but this window is not required it's just for ease of access for someone who doesn't want to code new commands. 
You can check it out [from here](https://github.com/PySimpleGUI/PySimpleGUI)

Once Python is set up, simply change the Twitch username (or Youtube channel ID) in ReshPlays_TEMPLATE.py, and you'll be ready to go.

# Example Useage
```py
# Start it running
if __name__ == "__main__":
    manager = exe('TwitchUserName')
    manager.countdown()
    manager.process_messages()
```

# Credit
This code is originally based off Wituz's Twitch Plays template, then expanded by DougDoug and DDarknut with help from Ottomated for the Youtube side. Modifications and clean up by catboy. Restructured for ease of use and access by wyatttwyattt!!
