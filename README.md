# ReshPlays

A modified version of [DougDoug's Twitch plays scripts](https://github.com/DougDougGithub/TwitchPlays), developed for DaBloodyResh with improvements to both structure and functionality.

This tool enables Twitch or YouTube chat to control your keyboard or mouse inputs, providing an interactive experience during live streams.

Key updates include restructuring the code to align with the existing pyautogui syntax, the addition of a GUI window for easier command creation, and an overall refactor to better maintainability.

## Installing

1. Download the project from [this link](https://github.com/DaBloodyResh/TwitchPlays/archive/refs/heads/main.zip) and extract the files to a folder on your computer.

2. If you don't already have Python installed, download it from [from here](<[https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe](https://www.python.org/downloads/release/python-3110/)>) (make sure to download Python 3.11 or newer).

   > **Important**: During installation, be sure to check the box "Add Python to environment variables" (under _Customize Install_ → _Advanced Options_).

3. Open a terminal or command prompt in the folder where you extracted the project files and run the following command to install the required dependencies:

```bash
pip install -r  requirements.txt
```

4. _(Optional)_ The project includes a GUI window for easier command creation, implemented using [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) This window is optional as it is simply for users who prefer not to code new commands manually.

5. Open `ReshPlays_TEMPLATE.py`, change the Twitch username (or YouTube channel ID) to your own, and you're ready to start using the tool.

6. Run the following command to start the app:
```bash
python ReshPlays_TEMPLATE.py
```

## Example Usage

```py
from TwitchPlays_CommandManager import CommandManager as exe
from ReshPlays_PyAutoGUI_Simplifier import shortHold

# Command is looking for the key word 'left' in the chat
@exe.command("left")
def move_left():
    shortHold("a", 1)  # Holds A key for 1 second

# Start it running
if __name__ == "__main__":
    manager = exe('TwitchUserName')  # Replace with your user name
    manager.countdown()  # Optional count down to give you some time 
    manager.process_messages()  # Starts listening for chat messages
```

## Credit

- **Wituz**: Original creator of the Twitch Plays template.
- **DougDoug**: and **DDarknut**: Expanded the core functionality.
- **Ottomated**: Helped with on Youtube implementation
- **catboy**: Refactored the code for improved structure and maintainability.
- **Wyatt**: Contributed to the UI development.

This project is based on the original Twitch Plays template by Wituz, with expansions by DougDoug and DDarknut and YouTube integration by Ottomated. The code was refactored for improved structure and maintainability by catboy, with UI development contributions from Wyatt.
