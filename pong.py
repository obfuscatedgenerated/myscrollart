import random, time, os
import bext

import keyboard

import math
from pysinewave import SineWave

from threading import Timer


def pitch2freq(pitch):
    return 261.625565 * 2 ** (pitch / 12)

def freq2pitch(freq):
    return abs(12 * math.log2(261.625565 / freq))



def beep(freq, secs, stereo=False, channel="lr"):  # cross platform winsound alternative
    if stereo:
        sinewave = SineWave(pitch=freq2pitch(freq), channels=2, channel_side=channel)
    else:
        sinewave = SineWave(pitch=freq2pitch(freq))
    sinewave.play()
    time.sleep(secs)
    sinewave.stop()

def non_blocking_beep(freq, secs, stereo=False, channel="lr"):
    if stereo:
        sinewave = SineWave(pitch=freq2pitch(freq), channels=2, channel_side=channel)
    else:
        sinewave = SineWave(pitch=freq2pitch(freq))
    sinewave.play()
    Timer(secs, sinewave.stop).start()


sound = True
ghost_for_float = False
centerline = True
stereo_sound = True

PAUSE_AMOUNT = 0.001

running = False

def header_render(width, text):
    return (" " * int((width - len(text))/2)) + text + " " * int((width - len(text))/2)

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

bext.bg("black")
bext.fg("white")
bext.hide()

clear()
width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
print("\n" * int((height-13)/2), end="")
print(header_render(width, "PONG"))
print("")
print(header_render(width, "Left Paddle: w, s"))
print(header_render(width, "Right Paddle: o, l"))
print("")
print(header_render(width, "Start / Unpause: space"))
print(header_render(width, "Pause: b"))
print("")
print(header_render(width, "Toggle sound (default: on): 1"))
print(header_render(width, "Toggle ball ghosting (default: off): 2"))
print(header_render(width, "Toggle center line (default: on): 3"))
print(header_render(width, "Toggle stereo output (default: on): 4"))


def main():
    L_score = 0
    R_score = 0
    L_pos = 0
    R_pos = 0
    ball_x = 0
    ball_y = 0

    width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)

    ball_x = int(width/2)
    ball_y = int(height/2)
    ball_dir = random.randint(0, 1)
    ball_spin = 0

    L_pos = int(height/2)
    R_pos = int(height/2)

    PADDLE_CHAR = "???"
    BALL_CHAR = "???"

    delta = 0

    while True:
        try:
            start_time = time.time()
            width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
            clear()
            #print(header_render(width, "PONG"))
            print(header_render(width, str(L_score) + " | " + str(R_score)))

            frame = ""
            for y in range(height):
                row = ""
                for x in range(width):
                    if x == int(ball_x) and ((y == int(ball_y) and not ghost_for_float) or (y == ball_y and ghost_for_float)):
                        row += BALL_CHAR
                    elif x == 5 and y in range(L_pos-2, L_pos+3):
                        row += PADDLE_CHAR
                    elif x == width-5 and y in range(R_pos-2, R_pos+3):
                        row += PADDLE_CHAR
                    elif x == int(width/2) and centerline:
                        row += "|"
                    else:
                        row += " "
                frame += row + "\n"
            print(frame.rstrip(), end="")

            if int(ball_x) <= 0:
                ball_x = int(width/2)
                ball_y = int(height/2)
                ball_dir = random.randint(0, 1)
                ball_spin = 0
                L_pos = int(height/2)
                R_pos = int(height/2)
                R_score += 1
                if sound:
                    beep(490, 0.257)
                else:
                    time.sleep(0.257)

            if int(ball_x) >= width:
                ball_x = int(width/2)
                ball_y = int(height/2)
                ball_dir = random.randint(0, 1)
                ball_spin = 0
                L_pos = int(height/2)
                R_pos = int(height/2)
                L_score += 1
                if sound:
                    beep(490, 0.257)
                else:
                    time.sleep(0.257)

            if int(ball_y) in range(L_pos-2, L_pos+3) and int(ball_x) == 5:
                ball_dir = 1
                ball_spin = ball_y - L_pos
                if sound:
                    non_blocking_beep(459, 0.096, stereo=stereo_sound, channel="l")
            
            if int(ball_y) in range(R_pos-2, R_pos+3) and int(ball_x) == width-5:
                ball_dir = 0
                ball_spin = ball_y - R_pos
                if sound:
                    non_blocking_beep(459, 0.096, stereo=stereo_sound, channel="r")
            
            if int(ball_y) <= 1 or int(ball_y) >= height-1:
                ball_spin = -ball_spin
                if sound:
                    non_blocking_beep(226, 0.066) # in the real game it should be 0.016 but that doesn't register here
            
            if ball_dir == 0:
                ball_x -= 100 * delta
            else:
                ball_x += 100 * delta
            
            ball_y += ball_spin/8
            
            if keyboard.is_pressed("w") and L_pos > 3:
                L_pos -= 1
            elif keyboard.is_pressed("s") and L_pos < height-3:
                L_pos += 1
                
            if keyboard.is_pressed("o") and R_pos > 3:
                R_pos -= 1
            elif keyboard.is_pressed("l") and R_pos < height-3:
                R_pos += 1
            
            if keyboard.is_pressed("b"):
                keyboard.wait(" ")

            bext.hide()
            print(flush=True)
            delta = time.time() - start_time
            time.sleep(PAUSE_AMOUNT)
        except (KeyboardInterrupt, SystemExit):
            clear()
            bext.fg("reset")
            print("\nBye!")
            break

def s_tog():
    global sound
    sound = not sound

def g_tog():
    global ghost_for_float
    ghost_for_float = not ghost_for_float

def c_tog():
    global centerline
    centerline = not centerline

def ss_tog():
    global stereo_sound
    stereo_sound = not stereo_sound

keyboard.add_hotkey("1", s_tog)
keyboard.add_hotkey("2", g_tog)
keyboard.add_hotkey("3", c_tog)
keyboard.add_hotkey("4", ss_tog)

while not running:
    kp = bext.getKey(blocking=True)
    if kp == " ":
        running = True
        main()
