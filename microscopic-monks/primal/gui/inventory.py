from kivy.graphics.instructions import RenderContext
from primal.engine.sprite import Sprite

class Inventory(Sprite):
    def __init__(self, pos, size, orientation: int = 0, **kwargs):
        super().__init__('Weapon-Inventory.png', pos, size, **kwargs)
        self.baseinv = Sprite(None, pos, size)

    def draw(self, canvas: RenderContext):
        self.baseinv.draw(canvas)

    '''
    Weapon Base is the actual backround that the weapons will be displayed on
    To Do: Make actual image, find actual image location
    '''