import math

from TLOA.core.constants import (MIRROR_CANNON_POS, MIRROR_OFFSET,
                                 MIRROR_DIAMETER, MIRROR_ANGLES)
from TLOA.entities import Entity

from kivy.properties import BoundedNumericProperty
from kivy.vector import Vector


class MirrorCannon(Entity):
    id = 'mirror_cannon'
    state = BoundedNumericProperty(4, min=0, max=5,
                                   errorhandler=lambda x: 0 if x < 0 else 5)

    def turn(self, direction: int):
        self.state += direction

    # Class Property to return the current angle.
    @property
    def angle(self):
        return MIRROR_ANGLES[self.state]

    # Class property to return end point & mid-point vectors of the mirror axis
    @property
    def mirror_axis(self):
        p0 = MIRROR_CANNON_POS + MIRROR_OFFSET

        p1 = p0 + Vector(
            round(0.5*MIRROR_DIAMETER*math.cos(math.radians(self.angle))),
            round(0.5*MIRROR_DIAMETER*math.sin(math.radians(self.angle)))
        )

        p2 = p0 - Vector(
            round(0.5*MIRROR_DIAMETER*math.cos(math.radians(self.angle))),
            round(0.5*MIRROR_DIAMETER*math.sin(math.radians(self.angle)))
        )

        return p0, p1, p2
