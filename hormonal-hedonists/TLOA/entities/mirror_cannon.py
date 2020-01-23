from TLOA.entities import Entity

from kivy.properties import BoundedNumericProperty


MIRROR_ANGLES = [
    75, 90, 105, 120, 135, 150
]


class MirrorCannon(Entity):

    id = 'mirror_cannon'
    state = BoundedNumericProperty(4, min=0, max=5,
                                   errorhandler=lambda x: 0 if x < 0 else 5)

    def turn(self, direction: int):
        self.state += direction

    @property
    def angle(self):
        return MIRROR_ANGLES[self.state]
