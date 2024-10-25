import time
import pyautogui
from TwitchPlays_CommandManager import CommandManager as exe
from TwitchPlays_KeyCodes import Key, HoldKey, ReleaseKey, HoldAndReleaseKey, ChanceKey

# Command functions
# Register a command with the @run.command("ChatMessage") function.
# Use the "HoldKey(KEYCODE)" function to permanently press and hold down a key.
# Use the "ReleaseKey(KEYCODE)" function to release a specific keyboard key.
# Use the "HoldAndReleaseKey(KEYCODE, SECONDS)" function press down a key for X seconds, then release it.
# Use the "ChanceKey(KEYCODE, SECONDS, CHANCE)" function holds and releases for a 1 in X chance.
# Use the pydirectinput library to press or move the mouse


# If the chat message is "left", then hold down the A key for 2 seconds
@exe.command("left")
def move_left():
    HoldAndReleaseKey(Key.A, 2)


# If the chat message is "right", then hold down the D key for 2 seconds
@exe.command("right")
def move_right():
    HoldAndReleaseKey(Key.D, 2)


# If message is "drive", then permanently hold down the W key
@exe.command("drive")
def drive_forward():
    ReleaseKey(Key.S)  # release brake key first
    HoldKey(Key.W)  # start permanently driving


# If message is "reverse", then permanently hold down the S key
@exe.command("reverse")
def reverse():
    ReleaseKey(Key.W)  # release drive key first
    HoldKey(Key.S)  # start permanently reversing


# Release both the "drive" and "reverse" keys
@exe.command("stop")
def stop():
    ReleaseKey(Key.W)
    ReleaseKey(Key.S)


# Press the spacebar for 0.7 seconds
@exe.command("brake")
def brake():
    HoldAndReleaseKey(Key.SPACE, 0.7)


# Press the left mouse button down for 1 second, then release it
@exe.command("shoot")
def shoot():
    pyautogui.mouseDown(button="left")
    time.sleep(1)
    pyautogui.mouseUp(button="left")


# Move the mouse up by 30 pixels
@exe.command("aim up")
def aim_up():
    pyautogui.moveRel(0, -30, relative=True)


# Move the mouse right by 200 pixels
@exe.command("aim right")
def aim_right():
    pyautogui.moveRel(200, 0, relative=True)


# Random chance 1-100 to jump
@exe.command("jump")
def jump():
    ChanceKey(Key.SPACE, 1, 100)


# Start the code running loop.
if __name__ == "__main__":
    manager = exe('TwitchUserName')
    manager.countdown()
    manager.process_messages()
