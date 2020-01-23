from TLOA.entities import Entity
from kivy.properties import BoundedNumericProperty, StringProperty, BooleanProperty

from enum import Enum

MIN_RES = 1
MAX_RES = 10

MAX_HEALTH = 100

MIN_SPEED = 5
MAX_SPEED = 10


class ShipType(Enum):
    BROWN = 0
    GOLDEN = 1


class Ship(Entity):
    _type = None
    health = BoundedNumericProperty(MAX_HEALTH, min=0, max=MAX_HEALTH,
                                    errorhandler=lambda x: 0 if x < 0 else MAX_HEALTH)
    fire_resistance = BoundedNumericProperty(MIN_RES, min=MIN_RES, max=MAX_RES,
                                             errorhandler=lambda x: MIN_RES if x < MIN_RES else MAX_RES)
    speed = BoundedNumericProperty(MIN_SPEED, min=MIN_SPEED, max=MAX_SPEED,
                                    errorhandler=lambda x: MIN_RES if x < MIN_RES else MAX_RES)
    destroyed = BooleanProperty(False)

    def take_damage(self, damage: int):
        # calculate health base on fire resistance. Can improve later
        health -= int(damage / self.fire_resistance)
    
    def on_health(self, instance, value):
        if self.health == 0:
            self.destroyed = True

class GoldenShip(Ship):
    _type = ShipType.GOLDEN
    fire_resistance = MAX_RES
    speed = MIN_SPEED


class BrownShip(Ship):
    _type = ShipType.BROWN
    fire_resistance = MIN_RES
    speed = MAX_SPEED