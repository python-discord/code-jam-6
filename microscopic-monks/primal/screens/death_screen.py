from primal.engine.screen import Screen
from primal.engine.camera import OrthographicCamera
from primal.engine.sprite import ColorSprite, Text


class DeathScreen(Screen):
    VP_WIDTH = 1280
    VP_HEIGHT = 720

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time = 0

        self.camera = OrthographicCamera(self.canvas, self.VP_WIDTH, self.VP_HEIGHT)
        self.camera.start_region()

        self.bg = ColorSprite(None, pos=(0, 0), size=(self.VP_WIDTH, self.VP_HEIGHT),
                              color=(0, 0, 0, 0))
        self.bg.draw(self.canvas)

        self.label = Text('Game Over', pos=(480, 350), height=80.0)
        self.label.set_color((0, 0, 0, 0))
        self.label.draw(self.canvas)

        self.hidden = True

        self.camera.end_region()

    def update(self, delta: float):
        self.time += delta

        if self.time < 1.5:
            self.bg.set_alpha(self.time / 1.5)
        else:
            if self.hidden:
                self.bg.set_alpha(1)
                self.label.set_color((1, 0, 0, 1))
                self.hidden = False
            if self.time > 5:
                from primal.screens.game_screen import GameScreen
                self.engine.set_screen(GameScreen())
                self.engine.remove_overlay()
