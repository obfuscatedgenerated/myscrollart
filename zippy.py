import random, time, os
import bext

PAUSE_AMOUNT = 0.001

colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white']

x = 0
y = 0
s = False
b = False
c = 0
while True:
    try:
        width = os.get_terminal_size()[0] - 2
        height = os.get_terminal_size()[1] - 2
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print(("\n"*y) + (x*" ")+"o", end="")
        if x >= width:
            s = True
            c += 1
            if b:
                y -= 1
            else:
                y += 1
            bext.fg(colors[c % len(colors)])
        if x <= 0:
            s = False
            c += 1
            if b:
                y -= 1
            else:
                y += 1
            bext.fg(colors[c % len(colors)])
        if y == height:
            b = True
        if y == 0:
            b = False
        if s:
            x -= 2
        else:
            x += 2
        print(flush=True)
        time.sleep(PAUSE_AMOUNT)
    except (KeyboardInterrupt, SystemExit):
        bext.fg("reset")
        print("\nBye!")
        break