from pathlib import Path

from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.properties import (
    NumericProperty, ReferenceListProperty)
from kivy.uix.widget import Widget


class Sprite(Widget):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)
    resource_dir = (Path('.') / 'resources').absolute()

    def __init__(self, image: str, pos: tuple = (0, 0), size: tuple = (50, 50), **kwargs) -> None:
        super().__init__(**kwargs)

        self.size = size
        self.pos = pos

        with self.canvas:
            self.bg_rect = Rectangle(source=(self.resource_dir / image).as_posix(),
                                     pos=self.pos,
                                     size=self.size)
        self.bind(pos=self.redraw)

    def redraw(self, *args) -> None:
        """Redraw the rectangle after moving the sprite."""
        x, y = self.pos
        if x < -2000 or x > Window.size[0] + 2000 or y < -2000 or y > Window.size[1] + 2000:
            return
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

    def __init__(self, image: str, pos: tuple = (0, 0), size: tuple = (50, 50), **kwargs) -> None:
        super().__init__(image, pos, size, **kwargs)

    def update(self) -> None:
        self.redraw()


class Terrain(Sprite):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)

    def __init__(self, perlin, pos: tuple = (0, 0), **kwargs) -> None:
        self.perlin = perlin
        self.m = int(perlin.shape[0] / 2 - 2 + pos[0] / 1000)
        self.n = int(perlin.shape[1] / 2 - 2 + pos[1] / 1000)
        a = perlin[self.m][self.n]
        if a > 0.75:
            image = 'i.png'
            self.type = 3
        elif a > 0.5:
            image = 'l.png'
            self.type = 2
        elif a > 0.25:
            image = 's.png'
            self.type = 1
        else:
            image = 'w.png'
            self.type = 0
        super().__init__(image, pos, (1000, 1000), **kwargs)

    def update(self):
        if self.pos[0] < -2000:
            self.pos[0] = 6000
            self.m += 8
        if self.pos[0] > 6000:
            self.pos[0] = -2000
            self.m -= 8
        if self.pos[1] < -2000:
            self.pos[1] = 5000
            self.n += 7
        if self.pos[1] > 5000:
            self.pos[1] = -2000
            self.n += 7
        a = self.perlin[self.m][self.n]
        if a > 0.75:
            image = 'i.png'
            self.type = 3
        elif a > 0.5:
            image = 'l.png'
            self.type = 2
        elif a > 0.25:
            image = 's.png'
            self.type = 1
        else:
            image = 'w.png'
            self.type = 0
        self.bg_rect.source = (self.resource_dir / image).as_posix()
        self.pos = (self.pos[0] + self.vel_x, self.pos[1] + self.vel_y)
        # dampen the velocity to come to a stop
        self.vel_x *= 0
        self.vel_y *= 0
