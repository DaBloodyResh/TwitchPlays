import time
from ReshPlays_CommandManager import CommandManager as exe
from ReshPlays_PyAutoGUI_Simplifier import *

@exe.command("left")
def move_left():
        shortHold('a', 2)

@exe.command("right")
def move_right():
    shortHold('d', 2)


@exe.command("forward")
def forward():
    press('w')
    time.sleep(0.5)
    release('s')


@exe.command("reverse")
def reverse():
    press('s')
    time.sleep(0.5)
    release('w')


@exe.command("stop")
def stop():
    release('w') 
    release('s')
    release('a')
    release('d')


@exe.command("brake")
def brake():
    press('space')
    time.sleep(0.75)
    release('space')


@exe.command("shoot")
def shoot ( ) :
     leftClickHold(2)


@exe.command("aim up")
def aim_up():
    relativeMove(0, -2)


@exe.command("aim right")
def aim_right():
    relativeMove(2, 0)


@exe.command('run')
def run():
    shortHoldWithKeyPress
    ('shift', 1, 'w', .25)
    time.sleep(3)
    autorun()


@exe.command("removeheal")
def removeheal():
        press('5')
        rightClick()
        time.sleep(0.2)
        leftClick()
        release('right')
        time.sleep(0.15)


@exe.command("noheals")
def noheals():
    num_repeats = 6

    for _ in range(num_repeats):
        press('5')
        rightClick()
        time.sleep(0.2)
        leftClick()
        release('right')
        time.sleep(0.15)


# everything under this is added through the Command Creator:


    print(template_lines)



    # Start the code running loop.
if __name__ == "__main__":
    manager = exe('DaBloodyResh')
    manager.countdown()
    manager.process_messages()
