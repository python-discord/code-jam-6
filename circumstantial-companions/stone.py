from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.vector import Vector
from itertools import product
from random import choice, random

GRAVITY = .02
FRICTION = .9
CHISEL_RADIUS = .0006
DISLODGE_VELOCITY = .0000001
MAX_VELOCITY = .000001
PEBBLE_RADIUS = 1.7
PEBBLE_COUNT = 10000
PEBBLE_SEGMENTS = 4
PEBBLE_COLORS = ((0.910, 0.784, 0.725),
                 (0.549, 0.514, 0.502),
                 (0.953, 0.816, 0.667),
                 (0.820, 0.694, 0.592),
                 (0.831, 0.796, 0.761),
                 (0.435, 0.329, 0.282),
                 (0.384, 0.207, 0.125))
POWER_SCALE = .001

def pebble_positions():
    pebble_count = int(PEBBLE_COUNT**.5)
    x_scale, y_scale = .5 / pebble_count, .75 / pebble_count
    x_offset = .25
    for y in range(pebble_count - 10):
        x_offset += (random() - .5) / 40
        for x in range(pebble_count):
            yield x_offset + x_scale * x, .001 + y_scale * y

    # Taper the top a bit to look more natural
    x_length = .5
    for y in range(y, y + 10):
        x_length *= .95
        pebble_count = int(pebble_count * .95)
        new_x_offset = (1 - x_length) / 2 + (x_offset - .25)
        x_scale = x_length / pebble_count
        for x in range(pebble_count):
            yield new_x_offset + x_scale * x, .001 + y_scale * y

class Pebble:
    def __init__(self, index, x, y, circles, x_dim, y_dim):
        self.index = index
        self.x = x
        self.y = y
        self.circles = circles # This is a pretty nasty hack, we'll change this later.
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.__velocity = 0.0, 0.0
        self.update = Clock.schedule_interval(self.step, 1/60)
        self.update.cancel()

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity_):
        """Start falling if velocity is over a certain threshold, else do nothing."""
        x, y = velocity_
        magnitude = (x**2 + y**2)**.5
        if magnitude < DISLODGE_VELOCITY:
            return
        if magnitude > MAX_VELOCITY:
            x *= MAX_VELOCITY / magnitude
            y *= MAX_VELOCITY / magnitude
        self.__velocity = velocity_
        self.update()

    def step(self, dt):
        """Gravity Physics"""
        vx, vy = self.__velocity
        vx *= FRICTION
        vy *= FRICTION
        vy -= GRAVITY

        self.x, self.y = max(0, min(1, self.x + vx)), max(0, self.y + vy)

        if self.y > 1:
            vy *= -1
        # I don't like this way of modifying circles in the Chisel widget, I'll rework it
        # after we get some working physics.
        self.circles[self.index].circle = (self.x * self.x_dim, self.y * self.y_dim,
                                           PEBBLE_RADIUS, 0, 360, PEBBLE_SEGMENTS)

        if not self.y:
            self.__velocity = 0.0, 0.0
            self.update.cancel()
        else:
            self.__velocity = vx, vy

class Chisel(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.parent:
            self.size = self.parent.size
        else:
            self.size = Window.size

        self.circles = []
        self.pebbles = []

        with self.canvas:
            for index, (x, y) in enumerate(pebble_positions()):
                Color(*choice(PEBBLE_COLORS))
                self.circles.append(Line(circle=(x * self.width, y * self.height,
                                                 PEBBLE_RADIUS, 0, 360, PEBBLE_SEGMENTS),
                                         width=PEBBLE_RADIUS))
                self.pebbles.append(Pebble(index, x, y, self.circles, self.width, self.height))

        def resize(*args):
            self.size = Window.size
            for i, pebble in enumerate(self.stone):
                x, y = pebble.pos
                self.circles[i].circle = (x * self.width, y * self.height,
                                          PEBBLE_RADIUS, 0, 360, PEBBLE_SEGMENTS)
        Window.bind(size=resize)

    def poke_power(self, touch_pos, pebble_x, pebble_y):
        """
        Returns the force vector of a poke.
        """
        tx, ty = touch_pos
        dx, dy = pebble_x - tx, pebble_y - ty
        distance = dx**2 + dy**2
        if distance > CHISEL_RADIUS:
            return 0.0, 0.0
        if not distance:
            distance = .0001
        power = POWER_SCALE / distance
        return power * dx, power * dy

    def poke(self, touch):
        """
        Apply a poke to each pebble.
        """
        for pebble in self.pebbles:
            pebble.velocity = self.poke_power(touch.spos, pebble.x, pebble.y)

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
