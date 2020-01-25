from primal.engine.screen import Screen
from primal.engine.camera import OrthographicCamera
from primal.engine.sprite import Terrain, Player, Rock, Tree

import random


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.camera = OrthographicCamera(self.canvas, 1280, 720)

        self.camera.start_region()
        self.seed = random.randint(0, 2**32 - 1)
        self.terrain = []
        self.tree = []
        self.rock = []
        for i in range(-2000, 7000, 1000):
            for j in range(-2000, 6000, 1000):
                temp_terrain = Terrain(self.seed, (i, j))
                temp_terrain.draw(self.canvas)
                self.terrain.append(temp_terrain)

                if temp_terrain.type == 0:
                    continue
                while True and random.randint(0, 1) == 1:
                    s = random.randint(50, 500)
                    temp_rock = Rock((i + random.randint(0, 1000), j + random.randint(0, 1000)),
                                     (s, s), random.randint(0, 359))
                    self.rock.append(temp_rock)

                if temp_terrain.type != 2:
                    continue
                while True and random.randint(0, 1) == 1:
                    s = random.randint(50, 100)
                    temp_tree = Tree((i + random.randint(0, 1000), j + random.randint(0, 1000)),
                                     (s, s), random.randint(0, 359))
                    self.tree.append(temp_tree)

        for i in self.tree:
            i.draw(self.canvas)

        for i in self.rock:
            i.draw(self.canvas)

        self.player = Player('testimg.png', (0, 0), (100, 100))
        self.player.draw(self.canvas)
        self.camera.end_region()

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

        self.camera.set_position(pos_x + 50, pos_y + 50)  # Updates the position
        self.camera.update()
