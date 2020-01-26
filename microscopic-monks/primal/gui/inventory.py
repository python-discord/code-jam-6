from kivy.graphics.instructions import RenderContext
from primal.engine.sprite import Sprite
from typing import Tuple, Union

# class Inventory(Sprite):
#     def __init__(self, image: Union[str, None], pos, size, orientation: int = 0, **kwargs):
#         self.baseinv = Sprite(image, pos, size)
#
#     def draw(self, canvas: RenderContext):
#         self.baseinv.draw(canvas)
#
#     '''
#     Weapon Base is the actual backround that the weapons will be displayed on
#     To Do: Make actual image, find actual image location
#     '''

from kivy.graphics.instructions import RenderContext

from primal.engine.sprite import ColorSprite, Item

import json


class Inventory:
    def __init__(self, pos):

        # accidentally switched items and grid, pls ignore that mistake
        self.items = []
        self.grid = []
        for i in range(10):
            self.grid.append(Sprite("blank.png", (pos[0] + 5, pos[1] + 60 * i + 5), (40, 40)))
        for i in range(10):
            self.items.append(ColorSprite(None, (pos[0], pos[1] + 60*i), (50, 50), (.0, .0, .0, .25)))

    def draw(self, canvas: RenderContext):
        for i in self.items:
            i.draw(canvas)
        for i in self.grid:
            i.draw(canvas)

    def update(self):
        with open((Sprite.resource_dir / "inventory.json").as_posix(), "r") as read_file:
            data = json.load(read_file)

        with open((Sprite.resource_dir / "items.json").as_posix(), "r") as read_file:
            itms = json.load(read_file)

        i = 0
        for item in data:
            try:
                self.grid[i].set_source(itms[item]["source"])
                self.grid[i].set_alpha(1)
            except:
                pass
            i += 1
