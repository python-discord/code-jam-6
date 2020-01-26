from pathlib import Path
from typing import Tuple, Union

from kivy.graphics.context_instructions import PushMatrix, PopMatrix
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import RenderContext, InstructionGroup
from kivy.graphics.context_instructions import Rotate
from kivy.uix.label import Label

import math
import json


class Text:
    def __init__(self, text: str, pos: Tuple[float, float], height: float):
        self.pos = pos
        self.height = height

        self.label = Label()
        self.label.font_size = 20
        self.label.bold = True
        self.label.text_size = 800, None
        self.color = Color(1, 1, 1, 1)
        self.rect = Rectangle(pos=pos)
        self.set_text(text)

    def set_text(self, text: str):
        self.label.text = text
        self.label.texture_update()
        ratio = self.label.texture_size[0] / self.label.texture_size[1]

        self.rect.size = ratio * self.height, self.height
        self.rect.texture = self.label.texture
        self.rect.texture.mag_filter = 'nearest'
        self.rect.texture.min_filter = 'nearest'

    def set_color(self, color: Tuple[float, float, float, float]):
        self.color.r = color[0]
        self.color.g = color[1]
        self.color.b = color[2]
        self.color.a = color[3]

    def draw(self, canvas: RenderContext):
        canvas.add(self.color)
        canvas.add(self.rect)
        canvas.add(Color(1, 1, 1, 1))


class Sprite:
    resource_dir = Path('.', 'primal', 'resources').absolute()
    try:
        f = open(resource_dir / "testimg.png")
        f.close()
    except FileNotFoundError:
        resource_dir = Path('.', 'resources').absolute()

    def __init__(self, image: Union[str, None], pos: Tuple[float, float],
                 size: Tuple[float, float], **kwargs) -> None:
        super().__init__(**kwargs)

        self.size = size
        self.pos = pos

        if image is None:
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        else:
            self.bg_rect = Rectangle(source=(Sprite.resource_dir / image).as_posix(),
                                     pos=self.pos, size=self.size)
        self.bg_rect.texture.mag_filter = 'nearest'
        self.bg_rect.texture.min_filter = 'nearest'

    def set_source(self, source: str):
        image = (Sprite.resource_dir / source).as_posix()
        if image != self.get_source():
            self.bg_rect.source = (Sprite.resource_dir / source).as_posix()
        self.bg_rect.texture.mag_filter = 'nearest'
        self.bg_rect.texture.min_filter = 'nearest'

    def get_source(self) -> str:
        return self.bg_rect.source

    def set_position(self, pos: Tuple[float, float]):
        self.pos = pos
        self.bg_rect.pos = pos

    def set_size(self, size: Tuple[float, float]):
        self.size = size
        self.bg_rect.size = size

    def get_size(self) -> Tuple[float, float]:
        return self.bg_rect.size

    def get_position(self) -> Tuple[float, float]:
        return self.pos

    def get_center(self):
        return self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2

    def draw(self, canvas: Union[RenderContext, InstructionGroup]):
        canvas.add(self.bg_rect)


class ColorSprite(Sprite):
    def __init__(self, image: Union[str, None], pos: Tuple[float, float],
                 size: Tuple[float, float], color: Tuple[float, float, float, float], **kwargs):
        super().__init__(image, pos, size, **kwargs)

        self.color = Color(*color)

    def draw(self, canvas: Union[RenderContext, InstructionGroup]):
        canvas.add(self.color)
        canvas.add(self.bg_rect)
        canvas.add(Color(1, 1, 1, 1))

    def set_alpha(self, alpha: float):
        self.color.a = alpha


class RotatableSprite(Sprite):
    def __init__(self, image: str, pos: Tuple[float, float],
                 size: Tuple[float, float], angle: float, **kwargs) -> None:
        super().__init__(image, pos, size, **kwargs)

        self.rotate = Rotate(angle=angle, origin=self.get_center())

    def set_angle(self, angle: float):
        self.rotate.angle = angle

    def get_rotation(self) -> float:
        return self.rotate.angle

    def draw(self, canvas: Union[RenderContext, InstructionGroup]):
        canvas.add(PushMatrix())
        canvas.add(self.rotate)
        canvas.add(self.bg_rect)
        canvas.add(PopMatrix())


class Player(RotatableSprite):
    SPEED = 300

    def __init__(self, image: str, pos: Tuple[float, float],
                 size: Tuple[float, float], angle: float, **kwargs):
        super().__init__(image, pos, size, angle, **kwargs)
        color = (0, 0, 0, 1)
        self.timer = 0

        self.in_hand = ColorSprite(None, (0, 0), (20, 20), (1, 1, 1, 1))
        self.in_hand.set_alpha(0)
        self.left_size = (20, size[1] * 0.3)
        self.right_size = (20, size[1] * 0.3)
        self.left = ColorSprite(None, (0, 0), self.left_size, color)
        self.right = ColorSprite(None, (0, 0), self.right_size, color)

    def set_rotation(self, n: Tuple[float, float]):
        pos = self.pos
        size = self.size
        self.rotate.origin = pos[0] + size[0] / 2, pos[1] + size[1] / 2

        x, y = n
        d = math.atan2(y - Window.size[1] / 2, x - Window.size[0] / 2) * 180 / math.pi
        self.rotate.angle = d

    def stop(self):
        if self.timer != 0:
            self.left_size = (20, self.left_size[1])
            self.right_size = (20, self.right_size[1])
            self.left.set_size(self.left_size)
            self.right.set_size(self.right_size)
            self.timer = 0

    def walk(self, delta):
        self.timer += delta * 6

        while self.timer >= math.pi * 2:
            self.timer -= math.pi * 2

        state = math.sin(self.timer)
        self.left_size = (20 + state * 35, self.left_size[1])
        self.right_size = (20 - state * 35, self.right_size[1])
        self.left.set_size(self.left_size)
        self.right.set_size(self.right_size)

    def change_item(self, image):
        if image is None:
            self.in_hand.set_alpha(0)
        else:
            self.in_hand.set_source(image)
            self.in_hand.set_alpha(1)

    def set_position(self, pos: Tuple[float, float]):
        self.left.set_position((pos[0], pos[1] + self.get_size()[1] * 0.2,))
        self.right.set_position((pos[0], pos[1] + self.get_size()[1] * 0.5))
        self.in_hand.set_position((pos[0] + 30, pos[1] - 10))
        super().set_position(pos)

    def draw(self, canvas: Union[RenderContext, InstructionGroup]):
        canvas.add(PushMatrix())
        canvas.add(self.rotate)
        self.left.draw(canvas)
        self.right.draw(canvas)
        canvas.add(self.bg_rect)
        self.in_hand.draw(canvas)
        canvas.add(PopMatrix())


class Item(Sprite):
    def __init__(self, name, player: Player, **kwargs):
        self.equipped = False
        self.inventory = False
        self.pos = Player.get_center()
        with open((self.resource_dir / "items.json").as_posix(), "r") as read_file:
            data = json.load(read_file)[name]
        super().__init__(data["source"], self.pos, data["size"], **kwargs)
        self.rotate = Rotate(angle=player.get_rotation(), origin=player.get_center())

    def draw(self, canvas: Union[RenderContext, InstructionGroup]):
        canvas.add(PushMatrix())
        canvas.add(self.rotate)
        canvas.add(self.bg_rect)
        canvas.add(PopMatrix())

    def equip(self):
        self.equipped = True

    def unequip(self):
        self.equipped = False
