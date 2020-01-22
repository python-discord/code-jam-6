from pathlib import Path
from typing import Tuple

from kivy.graphics.context_instructions import PushMatrix, PopMatrix
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.graphics.instructions import RenderContext
from kivy.graphics.context_instructions import Rotate
import math


class Sprite:
    resource_dir = (Path('.') / 'resources').absolute()

    def __init__(self, image: str, pos: Tuple[float, float] = (0, 0),
                 size: Tuple[float, float] = (50, 50), **kwargs) -> None:
        super().__init__(**kwargs)

        self.size = size
        self.pos = pos
        self.bg_rect = Rectangle(source=(self.resource_dir / image).as_posix(),
                                 pos=self.pos, size=self.size)

    def set_position(self, pos: Tuple[float, float]):
        self.pos = pos
        self.bg_rect.pos = pos

    def get_position(self) -> Tuple[float, float]:
        return self.pos

    def draw(self, canvas: RenderContext):
        canvas.add(self.bg_rect)


class Player(Sprite):
    SPEED = 200

    def __init__(self, image: str, pos: tuple = (0, 0), size: tuple = (200, 200), **kwargs) -> None:
        super().__init__(image, pos, size, **kwargs)

        self.rotate = Rotate(angle=0, origin=(pos[0] + size[0] / 2, pos[1] + size[1] / 2))

    def set_rotation(self, n: Tuple[float, float]):
        pos = self.pos
        size = self.size
        self.rotate.origin = pos[0] + size[0] / 2, pos[1] + size[1] / 2

        x, y = n
        d = math.atan2(y - Window.size[1] / 2, x - Window.size[0] / 2) * 180 / math.pi
        self.rotate.angle = d

    def draw(self, canvas: RenderContext):
        canvas.add(PushMatrix())
        canvas.add(self.rotate)
        canvas.add(self.bg_rect)
        canvas.add(PopMatrix())


class Terrain(Sprite):
    def __init__(self, perlin, pos: Tuple[float, float] = (0, 0), **kwargs) -> None:
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
