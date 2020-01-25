import math

from TLOA.core.constants import ATLAS_PATH

from kivy.uix.image import Image
from kivy.uix.widget import Widget

HP_BAR_X_OFFSET = 75
HP_BAR_Y_OFFSET = 150


class ShipView(Widget):
    def __init__(self, ship, source, pos, **kwargs):
        super().__init__(pos=pos, **kwargs)

        health = round(ship.health / 10) * 10
        x, y = self.pos
        self._hp_bar = Image(pos=(x + HP_BAR_X_OFFSET, y + HP_BAR_Y_OFFSET),
                             source=ATLAS_PATH.format(health))

        self._ship_image = Image(source=source, pos=self.pos)
        self._ship_image.size = self._ship_image.texture_size

        self.add_widget(self._hp_bar)
        self.add_widget(self._ship_image)

        ship.bind(health=self.on_health_change)
        self.bind(pos=self.on_pos_changed)

    def on_health_change(self, ship, value):
        health = math.ceil(value / 10) * 10
        self._hp_bar.source = ATLAS_PATH.format(health)
        # burn the ship if health < 50

        # destroy it if health is 0

    def on_pos_changed(self, ship_view, pos):
        x, y = self._ship_image.pos = self.pos
        self._hp_bar.pos = (x + HP_BAR_X_OFFSET, y + HP_BAR_Y_OFFSET)
        # TODO for burning effect
