from typing import Union
from kivy.graphics.instructions import RenderContext, InstructionGroup
from primal.engine.sprite import ColorSprite


class HealthBar:
    def __init__(self, pos, size, max_health: float = 100):
        self.max_health = max_health
        self.health = max_health

        self.size = size
        self.bg = ColorSprite(None, pos, size, (.0, .0, .0, .25))
        self.bar = ColorSprite(None, pos, size, (1, .0, .0, 1))

    def get_current_width(self) -> float:
        if self.health < 0:
            return 0.0
        if self.health > self.max_health:
            return self.size[1]

        return self.health * (self.size[0] / self.max_health)

    def get_health(self) -> float:
        return self.health

    def set_health(self, health: float):
        self.health = health
        self.bar.set_size((self.get_current_width(), self.size[1]))

    def draw(self, canvas: Union[InstructionGroup, RenderContext]):
        self.bg.draw(canvas)
        self.bar.draw(canvas)

    def set_alpha(self, alpha: float):
        self.bg.set_alpha(alpha / 4)
        self.bar.set_alpha(alpha)
