from TLOA.entities.entity import Entity

from kivy.properties import BoundedNumericProperty


class Mirror(Entity):

    state = BoundedNumericProperty(2, min=0, max=4,
                                   errorhandler=lambda x: 0 if x < 0 else 4)

    def turn(self, direction: int):
        self.state += direction
