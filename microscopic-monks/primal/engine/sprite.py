from pathlib import Path
from typing import Tuple

from kivy.graphics.context_instructions import PushMatrix, PopMatrix
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.graphics.instructions import RenderContext
from kivy.graphics.context_instructions import Rotate
import math
from primal.engine.perlin import sample


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
    def __init__(self, seed, pos: tuple = (0, 0), **kwargs) -> None:
        self.m = int(pos[0] / 10000)
        self.n = int(pos[1] / 10000)
        a = sample(self.m, self.n, seed=seed)
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

class Tree(Sprite):
    def __init__(self, pos: tuple = (0, 0), size: tuple = (50, 50), orientation: int = 0, **kwargs):
        super().__init__("topOfTree.png", pos, size, **kwargs)
        self.rotate = Rotate(angle=orientation, origin=(pos[0] + size[0] / 2, pos[1] + size[1] / 2))

    def draw(self, canvas: RenderContext):
        canvas.add(PushMatrix())
        canvas.add(self.rotate)
        canvas.add(self.bg_rect)
        canvas.add(PopMatrix())



class Rock(Sprite):
    def __init__(self, pos: tuple = (0, 0), size: tuple = (50, 50), orientation: int = 0, **kwargs):
        super().__init__("r.png", pos, size, **kwargs)
        self.rotate = Rotate(angle=orientation, origin=(pos[0] + size[0] / 2, pos[1] + size[1] / 2))

    def draw(self, canvas: RenderContext):
        canvas.add(PushMatrix())
        canvas.add(self.rotate)
        canvas.add(self.bg_rect)
        canvas.add(PopMatrix())