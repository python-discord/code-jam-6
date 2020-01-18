from pathlib import Path

from kivy.graphics import Rectangle
from kivy.properties import (
    NumericProperty, ReferenceListProperty)
from kivy.uix.widget import Widget


class Sprite(Widget):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)
    resource_dir = (Path('.') / 'resources').absolute()

    def __init__(self, image: str, pos: tuple = (0, 0), **kwargs) -> None:
        super().__init__(**kwargs)

        self.size = (50, 50)
        self.pos = pos

        with self.canvas:
            self.bg_rect = Rectangle(source=(self.resource_dir / image).as_posix(),
                                     pos=self.pos,
                                     size=self.size)
        self.bind(pos=self.redraw)

    def redraw(self, *args) -> None:
        """Redraw the rectangle after moving the sprite."""
        self.bg_rect.pos = self.pos

    def update(self) -> None:
        # update the position
        self.pos = (self.pos[0] + self.vel_x, self.pos[1] + self.vel_y)
        # dampen the velocity to come to a stop
        self.vel_x *= .75
        self.vel_y *= .75


class Player(Sprite):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)

    def __init__(self, image: str, pos: tuple = (0, 0), **kwargs) -> None:
        super().__init__(image, pos, **kwargs)

    def update(self) -> None:
        pass