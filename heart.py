from tkinter import *
from math import *
import random

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 8

def heart_function(t):
    x = 16 * (sin(t) ** 3)
    y = - (13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
    # 大小
    x *= IMAGE_ENLARGE
    y *= IMAGE_ENLARGE
    # 偏移
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)

def scatter_inside(x, y, beta=0.15):
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def shrink(x, y, ratio):
    force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.5)
    dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
    dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
    return x - dx, y - dy
class Heart:
    def __init__(self) -> None:
        self._points = set()
        self._extra_points = set()
        self._inside = set()
        self.all_points = {}
        self.build(2000)
    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((int(x), int(y)))
        #     边缘扩散
        for xx, yy in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(xx, yy, 0.05)
                self._extra_points.add((x, y))
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y)
            self._inside.add((int(x), int(y)))
    def calc_position(self, x, y, ratio):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.5)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy
    def calc(self, frame):
        calc_position = self.calc_position
        ratio = 10 * sin(frame / 10 * pi)
        all_points = []

        for x, y in self._points:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        for x, y in self._extra_points:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._inside:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[frame] = all_points
    def render(self, canvas, frame):
        for x, y, size in self.all_points[frame % 20]:
            canvas.create_rectangle(x, y, x+2, y+2, width=0, fill="#FF8888")

def draw(root: Tk, canvas: Canvas, heart :Heart, frame=0):
    canvas.delete('all')
    heart.render(canvas, frame)
    root.after(30, draw, root, canvas, heart, frame+1)

if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, bg = 'black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    for frame in range(20):
        heart.calc(frame)
    draw(root, canvas, heart)
    root.mainloop()