import random, time, os
import bext

import keyboard

import math
from pysinewave import SineWave


def pitch2freq(pitch):
    return 261.625565 * 2 ** (pitch / 12)


def freq2pitch(freq):
    return abs(12 * math.log2(261.625565 / freq))


def beep(freq, secs):  # cross platform winsound alternative
    sinewave = SineWave(pitch=freq2pitch(freq))
    sinewave.play()
    time.sleep(secs)
    sinewave.stop()

PAUSE_AMOUNT = 0.001

print("PONG")
print("")
print("Left Paddle: w, s")
print("Right Paddle: o, l")
print("")
print("Start: space")

running = False
ghost_for_float = False # set to True to make the ball Y not strictly an int at render (i.e. will blink when not on an exact pixel value rather than hopping between pixels)

def header_render(width, text):
    return (" " * int((width - len(text))/2)) + text + " " * int((width - len(text))/2)

def main():
    L_score = 0
    R_score = 0
    L_pos = 0
    R_pos = 0
    BALL_X = 0
    BALL_Y = 0

    width = os.get_terminal_size()[0] - 2
    height = os.get_terminal_size()[1] - 2

    BALL_X = int(width/2)
    BALL_Y = int(height/2)
    BALL_DIR = random.randint(0, 1)
    BALL_SPIN = 0

    L_pos = int(height/2)
    R_pos = int(height/2)

    paddle_char = "■"
    ball_char = "■"

    while True:
        try:
            width = os.get_terminal_size()[0] - 2
            height = os.get_terminal_size()[1] - 2
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
            #print(header_render(width, "PONG"))
            print(header_render(width, str(L_score) + " : " + str(R_score)))

            frame = ""
            for y in range(height):
                row = ""
                for x in range(width):
                    if x == BALL_X and ((y == int(BALL_Y) and not ghost_for_float) or (y == BALL_Y and ghost_for_float)):
                        row += ball_char
                    elif x == 5 and y in range(L_pos-2, L_pos+3):
                        row += paddle_char
                    elif x == width-5 and y in range(R_pos-2, R_pos+3):
                        row += paddle_char
                    else:
                        row += " "
                frame += row + "\n"
            print(frame.rstrip(), end="")

            if BALL_X == 0:
                BALL_X = int(width/2)
                BALL_Y = int(height/2)
                BALL_DIR = random.randint(0, 1)
                BALL_SPIN = 0
                L_pos = int(height/2)
                R_pos = int(height/2)
                R_score += 1
                beep(490, 0.257)

            if BALL_X == width:
                BALL_X = int(width/2)
                BALL_Y = int(height/2)
                BALL_DIR = random.randint(0, 1)
                BALL_SPIN = 0
                L_pos = int(height/2)
                R_pos = int(height/2)
                L_score += 1
                beep(490, 0.257)

            if int(BALL_Y) in range(L_pos-2, L_pos+3) and BALL_X == 5:
                BALL_DIR = 1
                BALL_SPIN = BALL_Y - L_pos
                #beep(459, 0.096)
            
            if int(BALL_Y) in range(R_pos-2, R_pos+3) and BALL_X == width-5:
                BALL_DIR = 0
                BALL_SPIN = BALL_Y - R_pos
                #beep(459, 0.096)
            
            if int(BALL_Y) <= 1 or int(BALL_Y) >= height-1:
                BALL_SPIN = -BALL_SPIN
            
            if BALL_DIR == 0:
                BALL_X -= 1
            else:
                BALL_X += 1
            
            BALL_Y += BALL_SPIN/8
            
            if keyboard.is_pressed("w") and L_pos > 3:
                L_pos -= 1
            elif keyboard.is_pressed("s") and L_pos < height-3:
                L_pos += 1
                
            if keyboard.is_pressed("o") and R_pos > 3:
                R_pos -= 1
            elif keyboard.is_pressed("l") and R_pos < height-3:
                R_pos += 1

            print(flush=True)
            time.sleep(PAUSE_AMOUNT)
        except (KeyboardInterrupt, SystemExit):
            bext.fg("reset")
            print("\nBye!")
            break

while not running:
    kp = bext.getKey(blocking=True)
    if kp == " ":
        running = True
        main()

bext.hide()
bext.bg("black")
bext.fg("white")