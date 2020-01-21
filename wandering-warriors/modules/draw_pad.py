from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Point, GraphicException
from math import sqrt


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
    def __init__(self, ** kwargs):
        super(DrawPad, self).__init__(** kwargs)
        self.in_pad = False

    def on_touch_down(self, touch):
        ud = touch.ud
        if (touch.pos[0] > self.pos[0]
           and touch.pos[0] < self.pos[0] + self.size[0]
           and touch.pos[1] > self.pos[1]
           and touch.pos[1] < self.pos[1] + self.size[1]):
            self.in_pad = True
            ud['group'] = g = str(touch.uid)
            pointsize = 1
            ud['color'] = 0
            with self.canvas:
                Color(0, 0, 0)
                ud['lines'] = [
                    Point(points=(touch.x, touch.y), source='particle.png',
                          pointsize=pointsize, group=g)]
            return True
        else:
            ud['lines'] = []

    def on_touch_move(self, touch):
        if(self.in_pad and touch.pos[0] > self.pos[0]
           and touch.pos[0] < self.pos[0] + self.size[0]
           and touch.pos[1] > self.pos[1]
           and touch.pos[1] < self.pos[1] + self.size[1]):
            ud = touch.ud

            points = ud['lines'][-1].points
            oldx, oldy = points[-2], points[-1]
            points = calculate_points(oldx, oldy, touch.x, touch.y)
            if points:
                try:
                    lp = ud['lines'][-1].add_point
                    for idx in range(0, len(points), 2):
                        lp(points[idx], points[idx + 1])
                except GraphicException:
                    pass

    def on_touch_up(self, touch):
        ud = touch.ud
        if self.in_pad:
            self.in_pad = False
            return (self.canvas.get_group(ud['group'])[1].points)
