from typing import Tuple

from TLOA.core.constants import MAX_SHIP_HEALTH

from kivy.event import EventDispatcher
from kivy.properties import BoundedNumericProperty
from kivy.uix.widget import Widget


class Entity(EventDispatcher):
    id: str = ''
    shape: Widget = None

    def step(self, dt, game):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class MovingEntity(Entity):
    health = BoundedNumericProperty(MAX_SHIP_HEALTH, min=0, max=MAX_SHIP_HEALTH,
                                    errorhandler=lambda x: 0 if x < 0 else MAX_SHIP_HEALTH)
    velocity: Tuple[float, float]

    def __init__(self, health, velocity, **kwargs):
        super().__init__(**kwargs)

        self.health = health
        self.velocity = velocity

    @property
    def is_dead(self):
        return self.health <= 0

    def step(self, dt, game):
        x, y = self.shape.pos
        dx, dy = self.velocity
        self.shape.pos = (x + dx, y + dy)
