from primal.engine.screen import Screen
from primal.engine.camera import OrthographicCamera
from primal.engine.sprite import Player
from primal.engine.world import World

from primal.gui.health import HealthBar
from primal.gui.inventory import Inventory


class GameScreen(Screen):
    VP_WIDTH = 1280
    VP_HEIGHT = 720

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.clicked_features = dict()
        self.last_clicked = 0.0

        self.camera = OrthographicCamera(self.canvas, self.VP_WIDTH, self.VP_HEIGHT)
        self.camera.start_region()

        self.zoom = 1.0

        self.world = World((0, 0))
        self.world.draw(self.canvas)

        self.player = Player('player.png', (0, 0), (40, 80), 0)
        self.player.draw(self.canvas)

        self.world.draw_top(self.canvas)

        self.camera.end_region()

        # render gui
        self.gui_camera = OrthographicCamera(self.canvas, self.VP_WIDTH, self.VP_HEIGHT)
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
        dx, dy = 0, 0

        if self.is_key_pressed('a'):
            dx -= Player.SPEED * delta
        if self.is_key_pressed('d'):
            dx += Player.SPEED * delta

        if self.is_key_pressed('w'):
            dy += Player.SPEED * delta
        if self.is_key_pressed('s'):
            dy -= Player.SPEED * delta

        if dx != 0.0 or dy != 0.0:
            px, py = self.player.get_center()

            dx, dy = self.process_player_position_deltas(px, py, dx, dy)

        # Check for clicked features
        self.last_clicked -= delta
        if self.last_clicked < 0:
            self.last_clicked = 0

        self.player.set_position((pos_x + dx, pos_y + dy))
        self.player.set_rotation(self.get_mouse_position())

        if self.last_clicked == 0:
            if 'left' in self.engine.mouse_keys:
                self.process_click()
                self.last_clicked = 0.03

        if 'scrolldown' in self.engine.mouse_keys:
            self.zoom += delta * 3
            self.zoom = min(1.6, self.zoom)
        elif 'scrollup' in self.engine.mouse_keys:
            self.zoom -= delta * 3
            self.zoom = max(0.68, self.zoom)

        new_clicked_features = dict()

        for feature, value in self.clicked_features.items():
            new_value = value - delta
            if new_value < 0:
                continue
            if new_value < 1:
                feature.set_alpha(new_value)
            new_clicked_features[feature] = new_value

        self.inventory.update()

        self.clicked_features = new_clicked_features
        self.engine.mouse_keys = set()

        self.world.update(self.player.get_center())

        self.camera.set_zoom(self.zoom)
        self.camera.set_position(*self.player.get_center())  # Updates the position
        self.camera.update()

    def process_player_position_deltas(self, px, py, dx, dy):
        chunk = self.world.get_chunk_from_coords((px + dx, py + dy))
        for feature in chunk.get_features():
            if feature.does_collide():
                dst = 40 + feature.get_size()[0]
                dst = (dst * dst) / 4
                if feature.distance_to((px, py + dy)) <= dst:
                    dy = 0

                if feature.distance_to((px + dx, py)) <= dst:
                    dx = 0

                if dy == 0 and dx == 0:
                    return 0.0, 0.0
        return dx, dy

    def process_click(self):
        mx, my = self.engine.mouse_position
        ww, wh = self.engine.window_size

        mx = self.VP_WIDTH - self.VP_WIDTH * mx / ww
        my = self.VP_HEIGHT - self.VP_HEIGHT * my / wh
        mx, my = self.camera.get_position_projection((mx, my))

        pos_x, pos_y = self.player.get_center()

        for chunk in self.world.get_chunk_in_range(1):
            features = chunk.get_features()
            clicked = False
            remove_features = set()

            for feature in features:
                if feature.distance_to((pos_x, pos_y)) < 15_000 \
                        and feature.collide_with((mx, my), (1, 1)):
                    feature.hit()
                    if feature.get_health() == 0:
                        remove_features.add(feature)
                        if feature in self.clicked_features:
                            del self.clicked_features[feature]
                    else:
                        self.clicked_features[feature] = 3.5
                    clicked = True
                    break

            for feature in remove_features:
                chunk.remove_feature(feature)

            if len(remove_features) != 0:
                self.world.render_chunk(chunk)

            if clicked:
                return
