import random, time, os
import bext


PAUSE_AMOUNT = 0.001


class Line:
    x = 0
    direction = 0

    def __init__(self, start_x, start_direction):
        width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
        assert start_x >= 0 and start_x < width, "start_x must be between 0 and width"
        assert start_direction in [-1, 1], "start_direction must be -1 or 1"
        self.x = start_x
        self.direction = start_direction
    
    def move(self):
        width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
        self.x += self.direction
        if self.x <= 0 or self.x >= width:
            self.direction = -self.direction
    
    def render(self):
        return "\\" if self.direction == 1 else "/"
    
    def getpos(self):
        return self.x

lines = []

width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
for i in range(1, int(width/10)):
    lines.append(Line(i*10, 1-(2*random.randint(0, 1))))

bext.hide()

while True:
    try:
        width, height = (os.get_terminal_size().columns-2, os.get_terminal_size().lines-2)
        renders = {}
        row = ""

        for line in lines:
            line.move()
            if line.getpos() in renders:
                renders[line.getpos()] = "X"
            else:
                renders[line.getpos()] = line.render()

        for x in range(width):
            if x in renders:
                row += renders[x]
            else:
                row += " "

        print(row, end="")
        print(flush=True)
        time.sleep(PAUSE_AMOUNT)
    except (KeyboardInterrupt, SystemExit):
        print("Bye!")
        break