import math
from random import choice, random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.vector import Vector
from PIL import Image
import numpy as np

GRAVITY = .02
FRICTION = .9
CHISEL_RADIUS = 6e-4
DISLODGE_VELOCITY = 1e-3
MAX_VELOCITY = .1
PEBBLE_IMAGE = 'boulder.png'
PEBBLE_RADIUS = 1.7
PEBBLE_COUNT = 1.5e4
PEBBLE_SEGMENTS = 4
POWER_SCALE = 1e2
MIN_POWER = 1e-5

CHISEL_RADIUS_RANGE = (0, 100)
DEFAULT_CHISEL_RADIUS = 15
CHISEL_POWER_RANGE = (0, 100)
DEFAULT_CHISEL_POWER = 45

def pebble_setup():
    """
    Determines initial pebble color and placement from an image's non-transparent pixels.
    """
    pebbles_per_line = int(PEBBLE_COUNT**.5)
    scale = 1 / pebbles_per_line
    x_scale = y_scale = .75 # How much of the screen we use
    x_offset, y_offset = (1 - x_scale) / 2, .01 # Lower-left corner offset of image

    with Image.open(PEBBLE_IMAGE) as image:
        w, h = image.size
        image = np.frombuffer(image.tobytes(), dtype=np.uint8)

    image = image.reshape((h, w, 4))

    for x in range(pebbles_per_line):
        x = scale * x
        for y in range(pebbles_per_line):
            y = scale * y
            sample_loc = int(y * h), int(x * w)
            r, g, b, a = image[sample_loc]
            if not a:
                continue
            pebble_x = x * x_scale + x_offset
            pebble_y = (1 - y) * y_scale + y_offset
            normalized_color = r / 255, g / 255, b / 255, a / 255
            yield normalized_color, pebble_x, pebble_y

def is_dislodged(velocity):
        """
        Return False if velocity isn't enough to dislodge a pebble, else return the clipped
        velocity vector.
        """
        x, y = velocity
        magnitude = (x**2 + y**2)**.5
        if magnitude < DISLODGE_VELOCITY:
            return False
        if magnitude > MAX_VELOCITY:
            x *= MAX_VELOCITY / magnitude
            y *= MAX_VELOCITY / magnitude
        return x, y

class Pebble:
    """
    This handles physics for dislodged pebbles. Deletes itself after pebbles reach the floor.
    """
    def __init__(self, index, circles, positions, x, y, pebbles, x_dim, y_dim, velocity):
        self.stopped = False
        self.index = index
        self.circles, self.positions = circles, positions
        self.x, self.y = x, y
        self.pebbles = pebbles
        self.x_dim, self.y_dim = x_dim, y_dim
        self.velocity = velocity
        self.update = Clock.schedule_interval(self.step, 0)

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
            del self.pebbles[self.index] # Remove reference // kill this object
        else:
            self.velocity = vx, vy

class Chisel(Widget):
    """
    Handles collision detection between pebbles and the hammer.  Creates Pebbles on collision.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize_event = Clock.schedule_once(lambda dt:None, 0)
        self.setup_background()

        self.pebbles = {}
        self.positions = []
        self.circles = []
        self.sound = SoundLoader.load('dig.wav')
        with self.canvas:
            for color, x, y in pebble_setup():
                Color(*color)
                self.positions.append((x, y))
                self.circles.append(Line(circle=(x * self.width, y * self.height,
                                                 PEBBLE_RADIUS, 0, 360, PEBBLE_SEGMENTS),
                                         width=PEBBLE_RADIUS))

        self.bind(size=self.delayed_resize, pos=self.delayed_resize)

        # TODO: Implement adjustable chisel radius and power
        self.set_radius(DEFAULT_CHISEL_RADIUS)
        self.set_power(DEFAULT_CHISEL_POWER)

    def setup_background(self):
        texture = CoreImage("assets/img/chisel_background.png").texture
        texture.wrap = "repeat"

        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.bg_rect = Rectangle(texture=texture)

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

    def delayed_resize(self, *args):
        self.resize_event.cancel()
        self.resize_event = Clock.schedule_once(lambda dt: self.resize(*args), .3)

    def resize(self, *args):
        self._update_bg_rect(*args)
        for i, (x, y) in enumerate(self.positions):
            self.circles[i].circle = (x * self.width, y * self.height,
                                      PEBBLE_RADIUS, 0, 360, PEBBLE_SEGMENTS)

    def poke_power(self, touch, pebble_x, pebble_y):
        """
        Returns the force vector of a poke.
        """
        tx, ty = touch.spos
        dx, dy = pebble_x - tx, pebble_y - ty
        distance = dx**2 + dy**2

        if distance > CHISEL_RADIUS:
            return 0.0, 0.0
        if not distance:
            distance = .0001

        tdx, tdy = touch.dsx, touch.dsy
        power = max(POWER_SCALE * (tdx**2 + tdy**2), MIN_POWER) / distance
        return power * dx, power * dy

    def poke(self, touch):
        """
        Apply a poke to each pebble.
        """
        for i, (x, y) in enumerate(self.positions):
            velocity = is_dislodged(self.poke_power(touch, x, y))
            if velocity: # Attach an object to the circle to move it.
                self.pebbles[i] = Pebble(i, self.circles,
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
