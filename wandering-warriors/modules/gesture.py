from kivy.gesture import Gesture
from .gesture_db import cun_1, cun_10


def check_gesture(points, gdb) -> int or None:
    g = Gesture()

    # convert raw DrawPad output to gesture compatible list
    point_list = list(zip(points[0::2], points[1::2]))
    g.add_stroke(point_list)
    g.normalize()

    # check if new gesture matches a known gesture
    g2 = gdb.find(g, minscore=0.70)

    if g2:
        if g2[1] == cun_1:
            return 1
        if g2[1] == cun_10:
            return 10

    return None
