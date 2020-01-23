import math

from kivy.uix.widget import Widget
from kivy.uix.image import Image

from TLOA.core.constants import SHIP_IMAGE_MAPPING, ATLAS_PATH

HP_BAR_X_OFFSET = 75
HP_BAR_Y_OFFSET = 100

class ShipView(Widget):
    def __init__(self, ship, **kwargs):
        # TODO consider to add lane as a property of ShipView
        self.core = ship
        super(ShipView, self).__init__(**kwargs)
        with self.canvas:
            # for ship
            img_source = ATLAS_PATH.format('brown_ship')
            self.view = Image(pos=self.pos, source=img_source)
            self.view.size = self.view.texture_size
            # for HP bar
            health = math.ceil(ship.health / 10) * 10
            # TODO fix hard code 200px
            self.hp_bar = Image(pos=(self.pos[0] + HP_BAR_X_OFFSET, self.pos[1] + HP_BAR_Y_OFFSET), source=ATLAS_PATH.format(health))
            # self.hp_bar = Image(pos=(self.pos[0], self.pos[1] + self.view.texture_size[1]), source=ATLAS_PATH.format(health))
            # TODO for burning effect
        self.core.bind(health=self.on_health_change)
        self.bind(pos=self.on_pos_changed) # workaround to handle pos change after init canvas

    def on_health_change(self, obj, value):
        health = math.ceil(value / 10) * 10
        self.hp_bar.source = ATLAS_PATH.format(health)
        # burn the ship if health < 50

        # destroy it if health is 0
    
    def on_pos_changed(self, *args):
        self.view.pos = self.pos
        self.hp_bar.pos = (self.pos[0] + HP_BAR_X_OFFSET, self.pos[1] + HP_BAR_Y_OFFSET)
        # self.hp_bar.pos = (self.pos[0], self.pos[1] + self.view.texture_size[1])
        # TODO for burning effect