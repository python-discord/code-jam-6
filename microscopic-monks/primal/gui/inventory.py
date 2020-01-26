from kivy.graphics.instructions import RenderContext

from primal.engine.sprite import Sprite
from primal.engine.sprite import ColorSprite

import json


class Inventory:
    def __init__(self, pos):
        self.items = []
        self.grid = []
        self.active = 0

        for i in range(10):
            self.items.append(Sprite("blank.png", (pos[0] + 5, pos[1] + 60 * i + 5), (40, 40)))

        for i in range(10):
            self.grid.append(
                ColorSprite(None, (pos[0], pos[1] + 60 * i), (50, 50), (1, 1, 1, .25)))

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
            data = json.load(read_file)

        with open((Sprite.resource_dir / "items.json").as_posix(), "r") as read_file:
            items = json.load(read_file)

        i = 0
        for item in data:
            try:
                self.items[i].set_source(items[item]["source"])
            except Exception:
                pass
            i += 1

    def update(self):
        with open((Sprite.resource_dir / "inventory.json").as_posix(), "r") as read_file:
            data = json.load(read_file)

        with open((Sprite.resource_dir / "items.json").as_posix(), "r") as read_file:
            items = json.load(read_file)

        i = 0
        for item in data:
            try:
                self.items[i].set_source(items[item]["source"])
            except Exception:
                pass
            i += 1
