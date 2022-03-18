import os, time, random
import bext

from threading import Timer

PAUSE_AMOUNT = 0.001

class RichTimer:
    def __init__(self, timeout, callback, info=None):
        self._timeout = timeout
        self._callback = callback
        self._info = info
        self._timer = Timer(self._timeout, self._callback, [info])
        self._timer.start()

    def cancel(self):
        self._timer.cancel()

class Positionable:
    def __init__(self, start_x, start_y, color):
        self._x = start_x
        self._y = start_y
        self._color = color
    
    def getPos(self):
        return (self._x, self._y)
    
    def setPos(self, x, y):
        self._x = x
        self._y = y
    
    def getColor(self):
        return self._color
    
    def setColor(self, color):
        self._color = color
    
    def _accelCallback(self, info=None):
        info["x_curr_speed"] += info["x_accel"] * info["i"]
        info["y_curr_speed"] += info["y_accel"] * info["i"]
        self._x += info["x_curr_speed"]
        self._y += info["y_curr_speed"]
        if not info["time_ticks"] == info["i"]:
            info["i"] += 1
            RichTimer(PAUSE_AMOUNT, self._accelCallback, info=info)
    
    def accelerateBy(self, x_accel, y_accel, time_ticks):
        RichTimer(PAUSE_AMOUNT, self._accelCallback, info={"i": 0, "x_curr_speed": 0, "y_curr_speed": 0, "x_accel": x_accel, "y_accel": y_accel, "time_ticks": time_ticks})

        

class Fireball(Positionable):
    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

class FireTracer(Positionable):
    def __init__(self, start_x, start_y, color, objective_ball):
        super().__init__(start_x, start_y, color)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    test = Positionable(0, 0, None)
    test.accelerateBy(0.001, 0, 100)
    while True:
        width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
        clear()
        frame = ""
        for i in range(height):
            row = ""
            for j in range(width):
                if i == int(test.getPos()[1]) and j == int(test.getPos()[0]):
                    row += "O"
                else:
                    row += " "
            frame += row + "\n"
        print(frame)
        time.sleep(PAUSE_AMOUNT)

bext.hide()
main()