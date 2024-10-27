# Me simplifying pyautogui for your leisure resh

import pyautogui
import time


def press(key):
    pyautogui.press(key)


def shortHold(key, duration=0.5):
    with pyautogui.hold(key):
        time.sleep(duration)


def release(key):
    # pressing with 0 delay basically, not rlly needed with hold but maybe
    pyautogui.press(key, interval=0)


def shortHoldWithKeyPress(key, hold_duration, key_to_press_during_hold, press_duration):
    pyautogui.keyDown(key)
    time.sleep(hold_duration)
    pyautogui.keyDown(key_to_press_during_hold)
    time.sleep(press_duration)
    pyautogui.keyUp(key_to_press_during_hold)
    pyautogui.keyUp(key)


# simplifies clicking
def leftClick():
    pyautogui.click(button='left')


# simplifies holding mouse buttons
def leftClickHold():
    pyautogui.mouseDown(button='left')
    time.sleep(duration)
    pyautogui.mouseUp(button='left')


def autorun():
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')


def rightClick():
    pyautogui.click(button='right')


def leftClickHold():
    pyautogui.mouseDown(button='right')
    time.sleep(duration)
    pyautogui.mouseUp(button='right')


# incase you wanna have something typed (probably not though)
def typeText(text, interval=0.1):
    pyautogui.write(text, interval=interval)


# simplifies moving the mouse
def moveMouseTo(x, y):
    pyautogui.moveTo(x, y)


# simplifies dragging the mouse
def dragMouseTo(x, y, duration=0.5):
    pyautogui.dragTo(x, y, duration=duration)


def relativeMove(x, y):
    pyautogui.moveRel(x * 50, y * 50, relative=True)
