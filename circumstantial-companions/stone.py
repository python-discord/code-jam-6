import math
from random import choice, random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.vector import Vector

GRAVITY = .02
FRICTION = .9
CHISEL_RADIUS = 6e-4
DISLODGE_VELOCITY = 1e-7
MAX_VELOCITY = .1
PEBBLE_RADIUS = 1.7
PEBBLE_COUNT = 1e4
PEBBLE_SEGMENTS = 4
PEBBLE_COLORS =((0.359, 0.33, 0.33),
                (0.383, 0.365, 0.352),
                (0.426, 0.377, 0.377),
                (0.383, 0.352, 0.352),
                (0.286, 0.257, 0.257),
                (0.304, 0.278, 0.278))
POWER_SCALE = 1e-3

CHISEL_RADIUS_RANGE = (0, 100)
DEFAULT_CHISEL_RADIUS = 15
CHISEL_POWER_RANGE = (0, 100)
DEFAULT_CHISEL_POWER = 45

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
        x_length *= .85
        pebble_count = int(pebble_count * .83)
        new_x_offset = (1 - x_length) / 2 + (x_offset - .25)
        x_scale = x_length / pebble_count
        for x in range(pebble_count):
            yield new_x_offset + x_scale * x, .001 + y_scale * y

def is_dislodged(velocity):
        x, y = velocity
        magnitude = (x**2 + y**2)**.5
        if magnitude < DISLODGE_VELOCITY:
            return False
        if magnitude > MAX_VELOCITY:
            x *= MAX_VELOCITY / magnitude
            y *= MAX_VELOCITY / magnitude
        return x, y

class Pebble:
    def __init__(self, index, circles, positions, x, y, pebbles, x_dim, y_dim, velocity):
        self.stopped = False
        self.index = index
        self.circles, self.positions = circles, positions
        self.x, self.y = x, y
        self.pebbles = pebbles
        self.x_dim, self.y_dim = x_dim, y_dim
        self.velocity = velocity
        self.update = Clock.schedule_interval(self.step, 0)
        self.update()

    def step(self, dt):
        """Gravity Physics"""
        x, y = self.x, self.y
        vx, vy = self.velocity
        vx *= FRICTION
        vy *= FRICTION
        vy -= GRAVITY

        # Bounce off walls
        if not 0 < x < 1:
            vx *= -1
        if y > 1:
            vy *= -1

        self.positions[self.index] = self.x, self.y = x + vx, max(0, y + vy)

        scaled_x, scaled_y = self.x * self.x_dim, self.y * self.y_dim
        self.circles[self.index].circle = (scaled_x, scaled_y,
                                           PEBBLE_RADIUS, 0, 360, PEBBLE_SEGMENTS)

        if not self.y:
            self.update.cancel()
            del self.pebbles[self.index] # Remove reference -- kill this object
        else:
            self.velocity = vx, vy

class Chisel(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = self.parent.size if self.parent else Window.size
        self.setup_background()

        self.pebbles = {}
        self.positions = [*pebble_positions()]
        self.circles = []
        self.sound = SoundLoader.load('dig.wav')
        with self.canvas:
            for index, (x, y) in enumerate(self.positions):
                Color(*choice(PEBBLE_COLORS))
                self.circles.append(Line(circle=(x * self.width, y * self.height,
                                                 PEBBLE_RADIUS, 0, 360, PEBBLE_SEGMENTS),
                                         width=PEBBLE_RADIUS))
        (self.parent if self.parent else Window).bind(size=self.resize)

        # TODO: Implement adjustable chisel radius and power
        self.set_radius(DEFAULT_CHISEL_RADIUS)
        self.set_power(DEFAULT_CHISEL_POWER)

    def setup_background(self):
        texture = CoreImage("assets/img/chisel_background.png").texture
        texture.wrap = "repeat"

        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.bg_rect = Rectangle(texture=texture)
            self._update_bg_rect(self)

        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

    def _get_uvsize(self):
        texture = self.bg_rect.texture
        return (math.ceil(self.width / texture.width),
                math.ceil(self.height / texture.height))

    def _get_background_size(self):
        texture = self.bg_rect.texture
        uv_width, uv_height = texture.uvsize
        return uv_width * texture.width, uv_height * texture.height

    def _update_bg_rect(self, instance, value=None):
        self.bg_rect.texture.uvsize = self._get_uvsize()
        self.bg_rect.texture = self.bg_rect.texture  # required to trigger update
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = self._get_background_size()

    def resize(self, *args):
        self.size = self.parent.size if self.parent else Window.size
        for i, pebble in enumerate(self.pebbles):
            self.circles[i].circle = (pebble.x * self.width, pebble.y * self.height,
                                      PEBBLE_RADIUS, 0, 360, PEBBLE_SEGMENTS)

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
        for i, (x, y) in enumerate(self.positions):
            velocity = is_dislodged(self.poke_power(touch.spos, x, y))
            if velocity: # Attach an object to the circle to move it.
                self.pebbles[i] = Pebble(i,
                                         self.circles,
                                         self.positions, x, y,
                                         self.pebbles,
                                         self.width, self.height,
                                         velocity)

    def on_touch_down(self, touch):
        self.poke(touch)
        self.sound.play()
        return True

    def on_touch_move(self, touch):
        self.poke(touch)
        return True

    def reset(self):
        print("TODO: Chisel.reset(self)")

    def set_radius(self, value):
        print("TODO: Chisel.set_radius(self, value)")
        self.radius = value

    def set_power(self, value):
        print("TODO: Chisel.set_power(self, value)")
        self.power = value


if __name__ == '__main__':
    class ChiselApp(App):
        def build(self):
            return Chisel()
    ChiselApp().run()
