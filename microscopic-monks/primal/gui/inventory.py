from kivy.graphics.instructions import RenderContext
from primal.engine.sprite import ColorSprite

class Inventory(Sprite):
    def __init__(self, pos, size, orientation: int = 0, **kwargs):
        super().__init__('Weapon-Inventory.png', pos, size, **kwargs)
        self.rotate = Rotate(angle=orientation, origin=self.get_center())

    def draw(self, canvas: RenderContext):
        self.bg.draw(canvas)
        self.bar.draw(canvas)

    '''
    Weapon Base is the actual backround that the weapons will be displayed on
    To Do: Make actual image, find actual image location
    '''