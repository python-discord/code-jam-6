from pathlib import Path

from kivy.graphics import Rectangle
from kivy.properties import (
    NumericProperty, ReferenceListProperty)
from kivy.uix.widget import Widget


class Sprite(Widget):
    resource_dir = (Path('.') / 'resources').absolute()

    def __init__(self, image, pos=(0, 0), **kwargs):
        super().__init__(**kwargs)

        self.size = (50, 50)
        self.pos = pos

        with self.canvas:
            self.bg_rect = Rectangle(source=(self.resource_dir / 'images/' / image).as_posix(),
                                     pos=self.pos,
                                     size=self.size)
        self.bind(pos=self.redraw)

    def redraw(self, *args) -> None:
        """Redraw the rectangle after moving the sprite."""
        self.bg_rect.pos = self.pos

    def update(self):
        raise NotImplementedError()


class Player(Sprite):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)

    def __init__(self, image, pos=(0, 0), **kwargs):
        super().__init__(image, pos, **kwargs)

    def update(self):
        # update the position
        self.pos = (self.pos[0] + self.vel_x, self.pos[1] + self.vel_y)
        # dampen the velocity to come to a stop
        self.vel_x *= .5
        self.vel_y *= .5
        # apply some downwards velocity
        self.vel_y -= 2
        # make sure we don't fall out of the world
        if self.pos[1] < 50:
            self.pos = (self.pos[0], 50)
