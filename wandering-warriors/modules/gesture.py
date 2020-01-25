from kivy.gesture import Gesture


def check_gesture(points, gdb):
    g = Gesture()

    # convert raw DrawPad output to gesture compatible list
    point_list = list(zip(points[0::2], points[1::2]))
    g.add_stroke(point_list)
    g.normalize()

    # check if new gesture matches a known gesture
    g2 = gdb.find(g, minscore=0.70)

    print(g2[1])
    return g2
