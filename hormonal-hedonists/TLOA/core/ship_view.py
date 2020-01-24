import math

from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import BooleanProperty
from kivy.logger import Logger

from TLOA.core.constants import SHIP_IMAGE_MAPPING, ATLAS_PATH

HP_BAR_X_OFFSET = 75
HP_BAR_Y_OFFSET = 100


class ShipView(Widget):
    core_destroyed = BooleanProperty(False)

    def __init__(self, ship, **kwargs):
        # TODO consider to add lane as a property of ShipView
        self.core = ship
        super(ShipView, self).__init__(**kwargs)
        with self.canvas:
            # for ship
            img_source = ATLAS_PATH.format(SHIP_IMAGE_MAPPING[ship._type])
            self.view = Image(pos=self.pos, source=img_source)
            self.view.size = self.view.texture_size
            # for HP bar
            health = math.ceil(ship.health / 10) * 10
            self.hp_bar = Image(pos=(self.pos[0] + HP_BAR_X_OFFSET, self.pos[1] + HP_BAR_Y_OFFSET),
                                source=ATLAS_PATH.format(health))
            # TODO for burning effect
        self.core.bind(health=self.on_health_change)
        self.core.bind(destroyed=self.on_core_destroyed)
        self.bind(pos=self.on_pos_changed)  # workaround to handle pos change after init canvas

    def on_health_change(self, obj, value):
        health = math.ceil(value / 10) * 10
        self.hp_bar.source = ATLAS_PATH.format(health)
        # burn the ship if health < 50

        # destroy it if health is 0

    def on_core_destroyed(self, obj, is_destroyed):
        Logger.debug(f'Ship view: handle core destroyed event')
        self.core_destroyed = is_destroyed
        if is_destroyed:
            # TODO add some effect if need
            pass

    def on_pos_changed(self, *args):
        self.view.pos = self.pos
        self.hp_bar.pos = (self.pos[0] + HP_BAR_X_OFFSET, self.pos[1] + HP_BAR_Y_OFFSET)
        # TODO for burning effect

    def set_new_core(self, ship):
        # unbind with old core
        self.core.unbind(health=self.on_health_change)
        self.core.unbind(destroyed=self.on_core_destroyed)
        self.core = ship
        self.core.bind(health=self.on_health_change)
        self.core.bind(destroyed=self.on_core_destroyed)
