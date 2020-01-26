from kivy.graphics.instructions import RenderContext

from primal.engine.sprite import Sprite
from primal.engine.sprite import ColorSprite
from primal.engine.feature import Feature

import json


class Inventory:
    def __init__(self, pos):
        self.item_data = None
        self.inventory_data = []

        self.items = []
        self.grid = []
        self.active = 0

        for i in range(10):
            self.items.append(Sprite("blank.png", (pos[0] + 5, pos[1] + 60 * i + 5), (40, 40)))

        for i in range(10):
            self.grid.append(
                ColorSprite(None, (pos[0], pos[1] + 60 * i), (50, 50), (1, 1, 1, .25)))

        self.load_inventory()
        self.set_ative(self.active)

    def set_ative(self, active: int):
        self.grid[self.active].set_alpha(.25)
        self.active = active
        self.grid[self.active].set_alpha(.8)

    def draw(self, canvas: RenderContext):
        for i in self.grid:
            i.draw(canvas)
        for i in self.items:
            i.draw(canvas)

    def load_inventory(self):
        with open((Sprite.resource_dir / "inventory.json").as_posix(), "r") as read_file:
            self.inventory_data = json.load(read_file)
            print(self.inventory_data)

        with open((Sprite.resource_dir / "items.json").as_posix(), "r") as read_file:
            self.item_data = json.load(read_file)

        i = 0
        for item in self.inventory_data:
            try:
                self.items[i].set_source(self.item_data[item[0]]['source'])
            except Exception:
                pass
            i += 1

    def add_item(self, feature: Feature):
        empty = None

        for index, item in enumerate(self.inventory_data):
            if len(item) == 0:
                if empty is None:
                    empty = index
                continue
            if item[0] == feature.type:
                self.inventory_data[index][1] += 1
                return

        if empty is not None:
            self.inventory_data[empty] = [feature.type, 1]
            self.items[empty].set_source(self.item_data[feature.type]['source'])
        elif len(self.inventory_data) != 10:
            self.inventory_data.append([feature.type, 1])
            source = self.item_data[feature.type]['source']
            self.items[len(self.inventory_data) - 1].set_source(source)
