from kivy.graphics.instructions import RenderContext
from primal.engine.sprite import Sprite
from typing import Tuple, Union

class Inventory(Sprite):
    def __init__(self, image: Union[str, None], pos, size, orientation: int = 0, **kwargs):
        self.baseinv = Sprite(image, pos, size)

    def draw(self, canvas: RenderContext):
        self.baseinv.draw(canvas)

    '''
    Weapon Base is the actual backround that the weapons will be displayed on
    To Do: Make actual image, find actual image location
    '''