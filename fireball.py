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
        info["x_curr_speed"] += info["x_accel"]
        info["y_curr_speed"] += info["y_accel"]
        self._x += info["x_curr_speed"]
        self._y += info["y_curr_speed"]
        if not info["time_ticks"] == info["i"]:
            info["i"] += 1
            RichTimer(PAUSE_AMOUNT, self._accelCallback, info=info)
        else:
            if info["callback"] is not None:
                info["callback"]()
    
    def accelerateBy(self, x_accel, y_accel, time_ticks, callback=None):
        assert time_ticks > 0, "time_ticks must be greater than 0"
        assert int(time_ticks) == time_ticks, "time_ticks must be an integer"
        RichTimer(PAUSE_AMOUNT, self._accelCallback, info={"i": 0, "x_curr_speed": 0, "y_curr_speed": 0, "x_accel": x_accel, "y_accel": y_accel, "time_ticks": time_ticks, "callback": callback})
    
    def accelerateTo(self, x_targ, y_targ, time_ticks, callback=None):
        assert time_ticks > 0, "time_ticks must be greater than 0"
        assert int(time_ticks) == time_ticks, "time_ticks must be an integer"
        # a = s - ut / 0.5t^2 (ut = 0 since init vel assumed to by 0)
        x_accel = (x_targ - self._x) / (0.5 * (time_ticks ** 2))
        y_accel = (y_targ - self._y) / (0.5 * (time_ticks ** 2))
        self.accelerateBy(x_accel, y_accel, time_ticks, callback)
        

class Fireball(Positionable):
    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)
        # accelerate to positions on the screen every so often

class FireTracer(Positionable):
    def __init__(self, start_x, start_y, color, objective_ball):
        super().__init__(start_x, start_y, color)
        self.objective_ball = objective_ball
        self.schedule_trace(random.randint(25, 500)/1000)
    
    def schedule_trace(self, delay):
        RichTimer(delay, self.trace)

    def _traceCallback(self, dir_vector, info=None):
        dir_mag = (dir_vector[0] ** 2 + dir_vector[1] ** 2) ** 0.5 # get magnitude of direction vector
        dir_norm = (dir_vector[0] / -dir_mag, dir_vector[1] / -dir_mag) # normalize direction vector
        random_accel = (random.uniform(0.005, 0.01) * dir_norm[0], random.uniform(0.005, 0.01) * dir_norm[1]) # get random acceleration vector in direction of direction vector
        self.accelerateBy(random_accel[0], random_accel[1], random.randint(25, 500))
        self.schedule_trace(random.randint(25, 500)/1000)
    
    def trace(self, info=None):
        dir_vector = (self._x - self.objective_ball.getPos()[0], self._y - self.objective_ball.getPos()[1])
        self.accelerateTo(self.objective_ball.getPos()[0], self.objective_ball.getPos()[1], random.randint(25, 500), lambda: self._traceCallback(dir_vector)) # accelerate to ball and then call the callback after


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
    test = Positionable(0, 0, None)
    test.accelerateTo(width/2, height/2, 100)
    test_trace = FireTracer(0, 0, None, test)
    while True:
        try:
            width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
            clear()
            frame = ""
            for i in range(height):
                row = ""
                for j in range(width):
                    if i == int(test.getPos()[1]) and j == int(test.getPos()[0]):
                        row += "T"
                    elif i == int(test_trace.getPos()[1]) and j == int(test_trace.getPos()[0]):
                        row += "t"
                    else:
                        row += " "
                frame += row + "\n"
            print(frame)
            time.sleep(PAUSE_AMOUNT)
        except (KeyboardInterrupt, SystemExit):
            print("Bye!")
            break

bext.hide()
main()