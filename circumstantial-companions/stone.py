import math
from random import choice, random

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
from PIL import Image
import numpy as np


GRAVITY = .02
FRICTION = .9
DISLODGE_VELOCITY = 1e-3
MAX_VELOCITY = .2

DEFAULT_PEBBLE_IMAGE = 'assets/img/boulder.png'
PEBBLE_COUNT = .75e4
PEBBLES_PER_LINE = int(PEBBLE_COUNT**.5)
PEBBLE_IMAGE_SCALE = .75

MIN_POWER = 1e-5

CHISEL_RADIUS_RANGE = (3e-4, 5e-3)
DEFAULT_CHISEL_RADIUS = 6e-4
CHISEL_POWER_RANGE = (50, 500)
DEFAULT_CHISEL_POWER = 100

BACKGROUND = 'assets/img/background.png'
SOUND = 'assets/sounds/dig.wav'

def get_pebble_size(width, height):
    scaled_w, scaled_h =  2 * PEBBLE_IMAGE_SCALE * width, 2 * PEBBLE_IMAGE_SCALE * height
    return scaled_w / PEBBLES_PER_LINE, scaled_h / PEBBLES_PER_LINE

def pebble_setup():
    """
    Determines initial pebble color and placement from an image's non-transparent pixels.
    """
    scale = 1 / PEBBLES_PER_LINE
    x_offset, y_offset = (1 - PEBBLE_IMAGE_SCALE) / 2, .1 # Lower-left corner offset of image

    with Image.open(DEFAULT_PEBBLE_IMAGE) as image:
        w, h = image.size
        image = np.frombuffer(image.tobytes(), dtype=np.uint8)

    image = image.reshape((h, w, 4))

    for x in range(PEBBLES_PER_LINE):
        x = scale * x
        for y in range(PEBBLES_PER_LINE):
            y = scale * y
            sample_loc = int(y * h), int(x * w)
            r, g, b, a = image[sample_loc]
            if not a:
                continue
            pebble_x = x * PEBBLE_IMAGE_SCALE + x_offset
            pebble_y = (1 - y) * PEBBLE_IMAGE_SCALE + y_offset
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
    def __init__(self, index, stone, x, y, z, velocity):
        self.index = index
        self.stone = stone
        self.x, self.y, self.z = x, y, z
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

        stone = self.stone
        stone.positions[self.index] = self.x, self.y, self.z = x + vx, max(0, y + vy), self.z

        scaled_x, scaled_y = self.x * stone.width, self.y * stone.height
        stone.pixels[self.index].size = stone.pebble_size
        stone.pixels[self.index].pos = scaled_x, scaled_y

        if not self.y:
            self.update.cancel()
            del stone.pebbles[self.index] # Remove reference // kill this object
        else:
            self.velocity = vx, vy


class Chisel(Widget):
    """
    Handles collision detection between pebbles and the hammer.  Creates Pebbles on collision.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sound = SoundLoader.load(SOUND)

        self.set_radius(DEFAULT_CHISEL_RADIUS)
        self.set_power(DEFAULT_CHISEL_POWER)

        self.setup_canvas()

        self.resize_event = Clock.schedule_once(lambda dt: None, 0)
        self.bind(size=self._delayed_resize, pos=self._delayed_resize)

    def setup_canvas(self):
        self.pebbles = {}
        self.positions = []
        self.pixels = []
        self.pebble_size = get_pebble_size(self.width, self.height)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.background = Rectangle(pos=self.pos, size=self.size, source=BACKGROUND)
            for (r, g, b, a), x, y in pebble_setup():
                scaled_x = x * self.width
                scaled_y = y * self.height
                for factor, depth in ((.5, 1), (1,0)):
                    Color(factor * r, factor * g, factor * b, a)
                    self.positions.append((x, y, depth))
                    self.pixels.append(Rectangle(pos=(scaled_x, scaled_y), size=self.pebble_size))
        self.background.texture.mag_filter = 'nearest'

    def _delayed_resize(self, *args):
        self.resize_event.cancel()
        self.resize_event = Clock.schedule_once(lambda dt: self.resize(*args), .3)

    def resize(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size
        self.pebble_size = get_pebble_size(self.width, self.height)
        for i, (x, y, z) in enumerate(self.positions):
            scaled_x = x * self.width
            scaled_y = y * self.height
            self.pixels[i].pos = (scaled_x, scaled_y)
            self.pixels[i].size = self.pebble_size

    def poke_power(self, touch, pebble_x, pebble_y):
        """
        Returns the force vector of a poke.
        """
        tx, ty = touch.spos
        dx, dy = pebble_x - tx, pebble_y - ty
        distance = dx**2 + dy**2

        if distance > self.chisel_radius:
            return 0.0, 0.0
        if not distance:
            distance = .0001

        tdx, tdy = touch.dsx, touch.dsy
        power = max(self.chisel_power * (tdx**2 + tdy**2), MIN_POWER) / distance
        return power * dx, power * dy

    def poke(self, touch):
        """
        Apply a poke to each pebble.
        """
        dislodged = {}
        for i, (x, y, z) in enumerate(self.positions):
            velocity = is_dislodged(self.poke_power(touch, x, y))
            if velocity and ((x, y) not in dislodged or dislodged[x, y]['z'] > z):
                    dislodged[x, y] = dict(i=i, z=z, velocity=velocity)
        for (x, y), info in dislodged.items():
                i, z, velocity = info.values()
                self.pebbles[i] = Pebble(i, self, x, y, z, velocity)

    def on_touch_down(self, touch):
        self.poke(touch)
        self.sound.play()
        return True

    def on_touch_move(self, touch):
        self.poke(touch)
        return True

    def reset(self):
        self.canvas.clear()
        self.setup_canvas()

    def set_radius(self, value):
        self.chisel_radius = value

    def set_power(self, value):
        self.chisel_power = value


if __name__ == '__main__':
    class ChiselApp(App):
        def build(self):
            return Chisel()
    ChiselApp().run()
