from typing import Tuple

from primal.gui.health import HealthBar
from primal.engine.sprite import RotatableSprite
from kivy.graphics.instructions import InstructionGroup


class Feature:
    def __init__(self, sprite: str, pos: Tuple[float, float], size: Tuple[float, float],
                 angle: float):

        hp_pos_x = (pos[0] + size[0] / 2) - 50
        hp_pos_y = pos[1]

        self.health_bar = HealthBar((hp_pos_x, hp_pos_y), (100, 7), 5)
        self.feature = RotatableSprite(sprite, pos, size, angle)
        self.alpha = 0

        self.set_alpha(self.alpha)

    def get_position(self) -> Tuple[float, float]:
        return self.feature.get_position()

    def get_center(self) -> Tuple[float, float]:
        return self.feature.get_center()

    def get_size(self) -> Tuple[float, float]:
        return self.feature.get_size()

    def set_alpha(self, alpha: float):
        self.alpha = alpha
        self.health_bar.set_alpha(self.alpha)

    def hit(self):
        self.set_alpha(1)
        health = self.health_bar.get_health()
        health = max(.0, health - 1)
        self.health_bar.set_health(health)

    def collide_with(self, pos, size) -> bool:
        sx, sy = self.get_position()
        sw, sh = self.get_size()
        sx -= 2 * sw

        ox, oy = pos
        ow, oh = size
        sx += 2 * sw
        return sx < ox + ow and sx + sw > ox and sy < oy + oh and sy + sh > oy

    def draw(self, canvas: InstructionGroup):
        self.feature.draw(canvas)
        self.health_bar.draw(canvas)
