from engine.sprite import Sprite

class Inventory(Sprite):
    resource_dir = (Path('..')/ 'primal'/'resources').absolute()
    def __init__(self, image: str, pos: tuple = (300, 0), size: tuple = (400, 400), **kwargs)):
       super().__init__(image, pos, size, **kwargs)

        '''
        Weapon Base is the actual backround that the weapons will be displayed on
        To Do: Make actual image, find actual image location
        '''
        weapon_base = Sprite('idk.png', )
        #Make the the thing
        