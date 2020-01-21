from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.core.window import Window

GRAVITY = 9.8
FRICTION = .9
CHISEL_RADIUS = .1


class Pebble:
    def __init__(self, pos):
        self.pos = pos
        self.velocity = 0.0
        self.update = Clock.schedule_interval(self.step, 0)
        self.update.cancel()

    def step(self, dt):
        """Gravity Physics"""
        pass

class Chisel(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = Window.size

        self.stone = [Pebble((.5, .5)), Pebble((.4, .4))]
        self.colors = []
        self.circles = []
        with self.canvas:
            for pebble in self.stone:
                self.colors.append(Color(.5, .5, .5, 1))
                x, y = pebble.pos

                self.circles.append(Line(circle=(x * self.width, y * self.height, 3), width=3))

        def resize(*args):
            self.size = Window.size
            for i, pebble in enumerate(self.stone):
                x, y = pebble.pos
                self.circles[i].circle = x * self.width, y * self.height, 3


        Window.bind(size=resize)

    def poke_power(self, touch_pos, pebble_pos):
        """
        Returns the force vector of a poke.
        """
        tx, ty = touch_pos
        px, py = pebble_pos
        dx, dy = px - tx, py - ty
        distance = dx**2 + dy**2
        if not distance:
            return
        return 2500 * dx / distance, 2500 * dy / distance

    def poke(self, touch):
        if touch.button == "left":
            for pebble in self.stone:
                pebble.velocity += self.poke_power(touch.spos, pebble.pos)

    def on_touch_down(self, touch):
        self.poke(touch)
        return True

    def on_touch_move(self, touch):
        self.poke(touch)
        return True

class ChiselApp(App):
    def build(self):
        return Chisel()


if __name__ == '__main__':
    ChiselApp().run()