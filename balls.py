import random, time, os
import bext

PAUSE_AMOUNT = 0.01

colors = ["red", "green", "blue", "yellow", "magenta", "cyan", "white"]

x = 0
s = False
c = 0
while True:
    try:
        width = os.get_terminal_size()[0] - 2
        height = os.get_terminal_size()[1] - 2
        print((x * "=") + "o", end="")
        if x == width:
            s = True
            c += 1
            bext.fg(colors[c % len(colors)])
        if x == 0:
            s = False
            c += 1
            bext.fg(colors[c % len(colors)])
        if s:
            x -= 1
        else:
            x += 1
        print(flush=True)
        time.sleep(PAUSE_AMOUNT)
    except (KeyboardInterrupt, SystemExit):
        bext.fg("reset")
        print("\nBye!")
        break
