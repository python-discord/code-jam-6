from primal.engine.screen import Screen
from primal.engine.camera import OrthographicCamera
from primal.engine.perlin import perlin_array
from primal.engine.sprite import Terrain, Player

import random


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.zoom = 0.5
        self.camera = OrthographicCamera(1280, 720)

        self.map = perlin_array()

        self.terrain = []
        for i in range(-2000, 7000, 1000):
            for j in range(-2000, 6000, 1000):
                temp_terrain = Terrain(self.map, (i, j))
                temp_terrain.draw(self.canvas)
                self.terrain.append(temp_terrain)

        self.player = Player('testimg.png', (200, 200), (100, 100))
        self.player.draw(self.canvas)

    def generate_terrain(self):
        tileObjects = []
        objects = {}
        for i in self.map:
            for j in i:
                if j < .25:
                    continue
                objects = {}
                while True:
                    rand = random.randint(1, 2)
                    if rand == 1:
                        while True:
                            x = random.randint(85, 915)
                            y = random.randint(85, 915)
                            broken = False
                            try:
                                for obj in objects["rock"]:
                                    if abs(obj[0] - x) < 80 or abs(obj[1] - y) < 80:
                                        broken = True
                                        break
                                if broken:
                                    continue
                                else:
                                    objects["rock"].append((x, y))
                                    break
                            except KeyError:
                                objects["rock"] = [(x, y)]
                    else:
                        break
                tileObjects.append(objects)
        print(tileObjects)

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

        self.camera.set_position(pos_x, pos_y)  # Updates the position
        self.set_projection_matrix(self.canvas, self.camera.get_projection())
