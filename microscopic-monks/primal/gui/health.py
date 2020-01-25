from kivy.graphics.instructions import RenderContext

from primal.engine.sprite import ColorSprite


class HealthBar:
    def __init__(self, pos, size, max_health: float = 100):
        self.max_health = max_health
        self.health = max_health

        self.size = size

        self.bg = ColorSprite(None, pos, size, (.75, .0, .0, .25))
        self.bar = ColorSprite(None, pos, size, (.25, .0, .0, .5))

    def get_current_width(self) -> float:
        if self.health < 0:
            return 0.0
        if self.health > self.max_health:
            return self.size[1]

        return self.health * (self.size[0] / self.max_health)

    def set_health(self, health: float):
        self.health = health
        self.bar.set_size((self.get_current_width(), self.size[1]))

    def draw(self, canvas: RenderContext):
        self.bg.draw(canvas)
        self.bar.draw(canvas)
