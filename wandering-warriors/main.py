from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Point, GraphicException
from math import sqrt

class Calculator(Screen):
    pass


class Settings(Screen):
    pass


class Screen_Holder(Screen):
    pass


class TopMenu(Widget):
    pass


class Abacus(Widget):
    pass


class Ledger(Widget):
    pass


class OperationsBar(Widget):
    pass

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

class CuneiformDrawingInput(FloatLayout):

    def on_touch_down(self, touch):
        ud = touch.ud
        if(touch.pos[0] > self.pos[0] and 
           touch.pos[0] < self.pos[0] + self.size[0] and 
           touch.pos[1] > self.pos[1] and 
           touch.pos[1] < self.pos[1] + self.size[1]):
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
        try:
            if(touch.pos[0] > self.pos[0] and 
               touch.pos[0] < self.pos[0] + self.size[0] and 
               touch.pos[1] > self.pos[1] and 
               touch.pos[1] < self.pos[1] + self.size[1]):
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
        except:
            pass
        #print(touch.pos)

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        ud = touch.ud
        return (self.canvas.get_group(ud['group'])[1].points)
        #self.canvas.remove_group(ud['group'])
        #self.remove_widget(ud['label'])


class Screen:
    def __init__(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Calculator(name='calculator'))

    def get_manager(self):
        return self.sm


class CalculatorApp(App):
    def build(self):
        Builder.load_file("calculator.kv")
        return Screen().get_manager()


if __name__ == "__main__":
    CalculatorApp().run()
''' 
        drawing_widget = CuneiformDrawingInput()
        drawing_widget.add_widget(Draw_Pad())
        holder = Screen_Holder(name="CuneiformDrawingInput")
        holder.add_widget(drawing_widget)
        self.sm.add_widget(holder)
'''