from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Point, GraphicException, Rectangle
from math import sqrt

from .gesture import check_gesture
from .gesture_db import load_gestures


def calculate_points(x1, y1, x2, y2, steps=1):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return
    o = []
    m = dist / steps
    for i in range(1, int(m)):
        mi = i / m
        lastx = x1 + dx * mi
        lasty = y1 + dy * mi
        o.extend([lastx, lasty])
    return o


class DrawPad(FloatLayout):
    def __init__(self, **kwargs):
        super(DrawPad, self).__init__(**kwargs)
        self.in_pad = False
        self.lines = []
        self.gdb = load_gestures()

        with self.canvas:
            self.border = []

            Color(1, 1, 1, 1)

            for i in range(4):
                self.border.append(Rectangle(source='assets/graphics/wood.png'))

        self.clear_button_src = 'assets/graphics/clear_sandbox.png'

        self.bind(pos=self.update, size=self.update)

        self.update()

    def update(self, *args):
        self.border[0].pos = self.pos
        self.border[0].size = (self.width, 16)

        self.border[1].pos = (self.x, self.y + self.height - 16)
        self.border[1].size = (self.width, 16)

        self.border[2].pos = self.pos
        self.border[2].size = (16, self.height)

        self.border[3].pos = (self.x + self.width - 16, self.y)
        self.border[3].size = (16, self.height)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        self.ud = touch.ud
        if (touch.pos[0] > self.pos[0]
                and touch.pos[0] < self.pos[0] + self.size[0]
                and touch.pos[1] > self.pos[1]
                and touch.pos[1] < self.pos[1] + self.size[1]):
            self.in_pad = True
            self.ud['group'] = g = str(touch.uid)
            pointsize = 3
            self.ud['color'] = 0
            with self.canvas.before:
                Color(.2, .1, .05, .08)
                self.ud['lines'] = [
                    Point(points=(touch.x, touch.y),
                          pointsize=pointsize, group=g)]
            return True
        else:
            self.ud['lines'] = []

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        if (self.in_pad and touch.pos[0] > self.pos[0]
                and touch.pos[0] < self.pos[0] + self.size[0]
                and touch.pos[1] > self.pos[1]
                and touch.pos[1] < self.pos[1] + self.size[1]):
            self.ud = touch.ud

            points = self.ud['lines'][-1].points
            oldx, oldy = points[-2], points[-1]
            points = calculate_points(oldx, oldy, touch.x, touch.y)
            if points:
                try:
                    lp = self.ud['lines'][-1].add_point
                    for idx in range(0, len(points), 2):
                        lp(points[idx], points[idx + 1])
                except GraphicException:
                    pass

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if self.in_pad:
            self.lines.append(self.ud['lines'])
            self.in_pad = False

            # check if line matches known gesture.
            value = check_gesture(self.ud['lines'][0].points, self.gdb)

            if value:
                print(f"Gesture value: {value}")
                # TODO: report value to relevant module
                # TODO: fade line out
                self.clear()

    def clear(self):
        for l in self.lines:
            l[0].points = []
