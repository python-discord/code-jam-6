from typing import Tuple

from primal.gui.health import HealthBar
from primal.engine.sprite import RotatableSprite
from kivy.graphics.instructions import InstructionGroup

from kivy.storage.jsonstore import JsonStore

store = JsonStore('inventory.py')


class Feature:
    def __init__(self, sprite: str, pos: Tuple[float, float], z: float, size: Tuple[float, float],
                 angle: float, type: str, collide: bool = False):
        hp_pos_x = (pos[0] + size[0] / 2) - 50
        hp_pos_y = pos[1]

        self.collide = collide
        self.type = type
        self.health_bar = HealthBar((hp_pos_x, hp_pos_y), (100, 7), 5)
        self.feature = RotatableSprite(sprite, pos, size, angle)
        self.alpha = 0
        self.z = z
        self.store = JsonStore('inventory.py')

        self.set_alpha(self.alpha)

    def does_collide(self) -> bool:
        return self.collide

    def get_z(self) -> float:
        return self.z

    def distance_to(self, pos) -> float:
        px, py = self.get_center()
        dx, dy = px - pos[0], py - pos[1]

        return dx * dx + dy * dy

    def get_position(self) -> Tuple[float, float]:
        return self.feature.get_position()

    def get_center(self) -> Tuple[float, float]:
        return self.feature.get_center()

    def get_health(self) -> float:
        return self.health_bar.get_health()

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

    # def broken(self):
    #     if self.get_health() < 0:
    #         self.store.put(sprite=3)
    #     else:
    #         pass
    #         # Not broken
