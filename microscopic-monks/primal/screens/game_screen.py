from primal.engine.screen import Screen
from primal.engine.camera import OrthographicCamera
from primal.engine.sprite import Terrain, Player

import random


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.camera = OrthographicCamera(self.canvas, 1280, 720)

        self.camera.start_region()
        self.seed = random.randint(0, 2**32 - 1)
        self.terrain = []
        for i in range(-2000, 7000, 1000):
            for j in range(-2000, 6000, 1000):
                temp_terrain = Terrain(self.seed, (i, j))
                temp_terrain.draw(self.canvas)
                self.terrain.append(temp_terrain)

        self.player = Player('testimg.png', (0, 0), (100, 100))
        self.player.draw(self.canvas)
        self.camera.end_region()

    # def generate_terrain(self):
    #     tileObjects = []
    #     objects = {}
    #     for i in self.map:
    #         for j in i:
    #             if j < .25:
    #                 continue
    #             objects = {}
    #             while True:
    #                 rand = random.randint(1, 2)
    #                 if rand == 1:
    #                     while True:
    #                         x = random.randint(85, 915)
    #                         y = random.randint(85, 915)
    #                         broken = False
    #                         try:
    #                             for obj in objects["rock"]:
    #                                 if abs(obj[0] - x) < 80 or abs(obj[1] - y) < 80:
    #                                     broken = True
    #                                     break
    #                             if broken:
    #                                 continue
    #                             else:
    #                                 objects["rock"].append((x, y))
    #                                 break
    #                         except KeyError:
    #                             objects["rock"] = [(x, y)]
    #                 else:
    #                     break
    #             tileObjects.append(objects)
    #     print(tileObjects)

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
