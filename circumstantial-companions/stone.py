from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.core.window import Window
from itertools import product

GRAVITY = .01
FRICTION = .9
CHISEL_RADIUS = .1
DISLODGE_VELOCITY = .1
MAX_VELOCITY = .001
PEBBLE_RADIUS = 2
PEBBLE_COUNT = 1000

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
        self.circles[self.index].circle = self.x * self.x_dim, self.y * self.y_dim, PEBBLE_RADIUS

        if not self.y:
            self.__velocity = 0.0, 0.0
            self.update.cancel()
        else:
            self.__velocity = vx, vy

class Chisel(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = Window.size # May want to change all Window.sizes to self.parent.size after completion

        pebble_count = int(PEBBLE_COUNT**.5)
        x_scale, y_scale = .5 / pebble_count, .75 / pebble_count

        self.positions = product([.25 + x_scale * x  for x in range(pebble_count)],
                                 [.01 + y_scale * y for y in range(pebble_count)])
        self.colors = []
        self.circles = []
        self.pebbles = []
        with self.canvas:
            for index, (x, y) in enumerate(self.positions):
                self.colors.append(Color(.5, .5, .5, 1))
                self.circles.append(Line(circle=(x * self.width, y * self.height, PEBBLE_RADIUS),
                                         width=PEBBLE_RADIUS))
                self.pebbles.append(Pebble(index, x, y, self.circles, self.width, self.height))


        def resize(*args):
            self.size = Window.size
            for i, pebble in enumerate(self.stone):
                x, y = pebble.pos
                self.circles[i].circle = x * self.width, y * self.height, PEBBLE_RADIUS
        Window.bind(size=resize)

    def poke_power(self, touch_pos, pebble_x, pebble_y):
        """
        Returns the force vector of a poke.
        """
        tx, ty = touch_pos
        dx, dy = pebble_x - tx, pebble_y - ty
        distance = dx**2 + dy**2
        if not distance:
            return
        return .01 * dx / distance, .01 * dy / distance

    def poke(self, touch):
        if touch.button == "left":
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