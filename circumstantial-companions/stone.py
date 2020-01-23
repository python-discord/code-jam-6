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

from mixins import RepeatingBackground

GRAVITY = .02
FRICTION = .9
CHISEL_RADIUS = 6e-4
DISLODGE_VELOCITY = 1e-3
MAX_VELOCITY = .1

PEBBLE_IMAGE = 'boulder.png'
PEBBLE_COUNT = 1.5e4
PEBBLES_PER_LINE = int(PEBBLE_COUNT**.5)
PEBBLE_SEGMENTS = 4
PEBBLE_IMAGE_SCALE = .75

POWER_SCALE = 1e2
MIN_POWER = 1e-5

CHISEL_RADIUS_RANGE = (0, 100)
DEFAULT_CHISEL_RADIUS = 15
CHISEL_POWER_RANGE = (0, 100)
DEFAULT_CHISEL_POWER = 45

def get_pebble_radius(width, height):
    scaled_w, scaled_h = PEBBLE_IMAGE_SCALE * width, PEBBLE_IMAGE_SCALE * height
    radius = max(scaled_w / PEBBLES_PER_LINE, scaled_h / PEBBLES_PER_LINE) * .36
    return radius

def pebble_setup():
    """
    Determines initial pebble color and placement from an image's non-transparent pixels.
    """
    scale = 1 / PEBBLES_PER_LINE
    x_offset, y_offset = (1 - PEBBLE_IMAGE_SCALE) / 2, .01 # Lower-left corner offset of image

    with Image.open(PEBBLE_IMAGE) as image:
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
    def __init__(self, index, stone, x, y, velocity):
        self.index = index
        self.stone = stone
        self.x, self.y = x, y
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
        stone.positions[self.index] = self.x, self.y = x + vx, max(0, y + vy)

        scaled_x, scaled_y = self.x * stone.width, self.y * stone.height
        stone.circles[self.index].width = stone.pebble_radius
        stone.circles[self.index].circle = (scaled_x, scaled_y,
                                            stone.pebble_radius, 0, 360, PEBBLE_SEGMENTS)

        if not self.y:
            self.update.cancel()
            del stone.pebbles[self.index] # Remove reference // kill this object
        else:
            self.velocity = vx, vy


class Chisel(RepeatingBackground, Widget):
    """
    Handles collision detection between pebbles and the hammer.  Creates Pebbles on collision.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize_event = Clock.schedule_once(lambda dt:None, 0)
        self.setup_background("assets/img/chisel_background.png", 0.1, (0.4, 0.4, 0.4, 1))
        self.sound = SoundLoader.load('dig.wav')

        # TODO: Implement adjustable chisel radius and power
        self.set_radius(DEFAULT_CHISEL_RADIUS)
        self.set_power(DEFAULT_CHISEL_POWER)

        self.setup_canvas()

    def setup_canvas(self):
        self.pebbles = {}
        self.positions = []
        self.circles = []
        pebble_radius = self.pebble_radius = get_pebble_radius(self.width, self.height)
        with self.canvas:
            for color, x, y in pebble_setup():
                Color(*color)
                self.positions.append((x, y))
                self.circles.append(Line(circle=(x * self.width, y * self.height,
                                                 pebble_radius, 0, 360, PEBBLE_SEGMENTS),
                                         width=pebble_radius))

    def resize(self, instance, value):
        self.update_background(instance, value)
        self.pebble_radius = get_pebble_radius(self.width, self.height)
        for i, (x, y) in enumerate(self.positions):
            self.circles[i].width = self.pebble_radius
            self.circles[i].circle = (x * self.width, y * self.height,
                                      self.pebble_radius, 0, 360, PEBBLE_SEGMENTS)

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
                self.pebbles[i] = Pebble(i, self, x, y, velocity)

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
