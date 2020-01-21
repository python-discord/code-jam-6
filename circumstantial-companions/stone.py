from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color

GRAVITY = 9.8
FRICTION = .9
CHISEL_RADIUS = .1


class Pebble(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with self.canvas.before:
            self.color = Color(.1, .1, .1, 1) # Gray pebble color -- well change this to slightly deviate
        self.size = 5, 5