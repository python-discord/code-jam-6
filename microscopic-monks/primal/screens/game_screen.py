from primal.engine.screen import Screen
from primal.engine.camera import OrthographicCamera
from primal.engine.sprite import Player
from primal.engine.world import World

from primal.gui.health import HealthBar
from primal.gui.inventory import Inventory


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.camera = OrthographicCamera(self.canvas, 1280, 720)
        self.camera.start_region()

        self.world = World((0, 0))
        self.world.draw(self.canvas)

        self.player = Player('testimg.png', (0, 0), (100, 100), 0)
        self.player.draw(self.canvas)

        self.camera.end_region()

        # render gui
        self.gui_camera = OrthographicCamera(self.canvas, 1280, 720)
        self.gui_camera.start_region()

        self.health_bar = HealthBar((20, 680), (250, 20), 100.0)
        self.health_bar.draw(self.canvas)
        self.health_bar.set_health(80)

        self.inventory = Inventory((20, 20))
        self.inventory.draw(self.canvas)



        self.gui_camera.end_region()

    def update(self, delta: float):
        # Maybe move it to player update?
        pos_x, pos_y = self.player.get_position()

        if self.is_key_pressed('a'):
            pos_x -= Player.SPEED * delta
        elif self.is_key_pressed('d'):
            pos_x += Player.SPEED * delta

        if self.is_key_pressed('w'):
            pos_y += Player.SPEED * delta
        elif self.is_key_pressed('s'):
            pos_y -= Player.SPEED * delta

        self.player.set_position((pos_x, pos_y))
        self.player.set_rotation(self.get_mouse_position())

        self.world.update(self.player.get_center())
        self.camera.set_position(*self.player.get_center())  # Updates the position
        self.camera.update()
