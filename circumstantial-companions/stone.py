import math
import json
from pathlib import Path
from random import choice, random

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from PIL import Image
import numpy as np
import simpleaudio as sa # sdl2_mixer non-functional for me so I resorted to this --salt-die

GRAVITY = .02
FRICTION = .9
DISLODGE_VELOCITY = 1e-3
MAX_VELOCITY = .2

PEBBLE_COUNT = 7e3 # per layer.
PEBBLE_IMAGE_SCALE = .75

CHISEL_RADIUS = 6e-4
MIN_POWER = 1e-5
CHISEL_POWER = 100

BACKGROUND = str(Path('assets', 'img', 'background.png'))
SOUND = tuple(str(Path('assets', 'sounds', f'00{i}.wav')) for i in range(1, 5))

def get_image_and_aspect(file):
    """
    Returns image and the correct ratio of pebbles per row and column from PEBBLE_COUNT and
    image height and width.
    """
    with Image.open(file) as image:
        w, h = image.size
        image = np.frombuffer(image.tobytes(), dtype=np.uint8)
    image = image.reshape((h, w, 4))

    pebbles_per_row = (PEBBLE_COUNT * w / h)**.5
    pebbles_per_column = pebbles_per_row * h / w

    return image, int(pebbles_per_row), int(pebbles_per_column)

PEBBLE_IMAGES = (Path("assets", "img", "boulder", f"{i}.png") for i in range(4))
PEBBLE_IMAGES = tuple(get_image_and_aspect(image) for image in PEBBLE_IMAGES)
CURRENT_IMAGE = list(choice(PEBBLE_IMAGES))

def pebble_setup():
    """
    Determines initial pebble color and placement from an image's non-transparent pixels.
    """
    image, pebbles_per_row, pebbles_per_column = CURRENT_IMAGE
    x_scale, y_scale = 1 / pebbles_per_row, 1 / pebbles_per_column
    x_offset, y_offset = (1 - PEBBLE_IMAGE_SCALE) / 2, .1 # Lower-left corner offset of image.
    h, w, _ = image.shape

    for x in range(pebbles_per_row):
        x = x_scale * x
        for y in range(pebbles_per_column):
            y = y_scale * y
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
        vx, vy = self.velocity
        vx *= FRICTION
        vy *= FRICTION
        vy -= GRAVITY

        # Bounce off walls
        x, y = self.x, self.y
        if not 0 < x < 1:
            vx *= -1
        if y > 1:
            vy *= -1

        self.velocity = vx, vy
        self.x, self.y = x + vx, max(0, y + vy)

        self.update_canvas()

    def update_canvas(self):
        stone = self.stone
        stone.positions[self.index] = x, y, _ = self.x, self.y, self.z
        scaled_x, scaled_y = x * stone.width, y * stone.height
        stone.pixels[self.index].pos = scaled_x, scaled_y
        stone.pixels[self.index].size = stone.pebble_size

        if not self.y:
            self.update.cancel()
            del stone.pebbles[self.index] # Remove reference // kill this object


class Chisel(Widget):
    """
    Handles collision detection between pebbles and the hammer.  Creates Pebbles on collision.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sounds = tuple(sa.WaveObject.from_wave_file(sound) for sound in SOUND)
        self.setup_canvas()
        self.resize_event = Clock.schedule_once(lambda dt: None, 0)
        self.bind(size=self._delayed_resize, pos=self._delayed_resize)

    def get_pebble_size(self):
        """Calculate the correct pebble size so we have no gaps in our stone."""
        scaled_w = PEBBLE_IMAGE_SCALE * self.width
        scaled_h = PEBBLE_IMAGE_SCALE * self.height
        _, pebbles_per_row, pebbles_per_column = CURRENT_IMAGE
        return scaled_w / pebbles_per_row, scaled_h / pebbles_per_column

    def setup_canvas(self):
        self.pebbles = {}
        self.positions = []
        self.colors = []
        self.pixels = []
        self.pebble_size = self.get_pebble_size()
        with self.canvas:
            self.background_color = Color(1, 1, 1, 1)
            self.background = Rectangle(pos=self.pos, size=self.size, source=BACKGROUND)
            for depth, color_scale in enumerate((.4, .6, 1)):
                for (r, g, b, a), x, y in pebble_setup():
                    color = color_scale * r, color_scale * g, color_scale * b, a
                    Color(*color)
                    scaled_x = x * self.width
                    scaled_y = y * self.height
                    self.colors.append(color)
                    self.positions.append((x, y, depth))
                    self.pixels.append(Rectangle(pos=(scaled_x, scaled_y), size=self.pebble_size))
        self.background.texture.mag_filter = 'nearest'

    def _delayed_resize(self, *args):
        self.resize_event.cancel()
        self.resize_event = Clock.schedule_once(lambda dt: self.resize(*args), .3)

    def resize(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size
        self.pebble_size = self.get_pebble_size()
        for i, (x, y, z) in enumerate(self.positions):
            scaled_x = x * self.width
            scaled_y = y * self.height
            self.pixels[i].pos = scaled_x, scaled_y
            self.pixels[i].size = self.pebble_size

    def poke_power(self, tx, ty, touch_velocity, pebble_x, pebble_y):
        """
        Returns the force vector of a poke.
        """
        dx, dy = pebble_x - tx, pebble_y - ty
        distance = dx**2 + dy**2

        if distance > CHISEL_RADIUS:
            return 0, 0
        if not distance:
            distance = 1e-4

        power = max(CHISEL_POWER * touch_velocity, MIN_POWER) / distance
        return power * dx, power * dy

    def poke(self, touch):
        """
        Apply a poke to each pebble ignoring pebbles that are below other pebbles.
        """
        tx, ty = touch.spos
        tdx, tdy = touch.dsx, touch.dsy
        touch_velocity = tdx**2 + tdy**2
        dislodged = {}

        for i, (x, y, z) in enumerate(self.positions):
            velocity = is_dislodged(self.poke_power(tx, ty, touch_velocity, x, y))
            if velocity and ((x, y) not in dislodged or dislodged[x, y][0] < z):
                    dislodged[x, y] = (z, i, velocity)

        for (x, y), (z, i, velocity) in dislodged.items():
                self.pebbles[i] = Pebble(i, self, x, y, z, velocity)

    def on_touch_down(self, touch):
        self.poke(touch)
        choice(self.sounds).play()
        return True

    def on_touch_move(self, touch):
        self.poke(touch)
        return True

    def reset(self):
        CURRENT_IMAGE[:] = list(choice(PEBBLE_IMAGES))
        self.canvas.clear()
        self.setup_canvas()

    def save(self, path_to_file):
        _, pebbles_per_row, pebbles_per_column = CURRENT_IMAGE
        positions = []
        colors = []
        for (x, y, z), color in zip(self.positions, self.colors):
            if y:
                positions.append((x, y, z))
                colors.append(color)

        pebble_dict = {'positions': positions,
                       'colors': colors,
                       'aspect': (pebbles_per_row, pebbles_per_column)}
        with open(path_to_file, 'w') as file:
            json.dump(pebble_dict, file)

    def load(self, path_to_file):
        with open(path_to_file, 'r') as file:
            pebble_dict = json.load(file)
        self.pebbles = {}
        self.positions = pebble_dict['positions']
        self.colors = pebble_dict['colors']
        CURRENT_IMAGE[1:] = pebble_dict['aspect']
        self.pixels = []
        self.pebble_size = self.get_pebble_size()
        self.canvas.clear()
        with self.canvas:
            self.background_color = Color(1, 1, 1, 1)
            self.background = Rectangle(pos=self.pos, size=self.size, source=BACKGROUND)
            for color, (x, y, z) in zip(self.colors, self.positions):
                Color(*color)
                scaled_x = x * self.width
                scaled_y = y * self.height
                self.pixels.append(Rectangle(pos=(scaled_x, scaled_y), size=self.pebble_size))
        self.background.texture.mag_filter = 'nearest'

    def export_png(self, path_to_file, transparent=False):
        if transparent:
            self.background_color.a = 0
        self.export_to_png(path_to_file)
        self.background_color.a = 1


if __name__ == '__main__':
    class ChiselApp(App):
        def build(self):
            return Chisel()
    ChiselApp().run()
