from primal.engine.screen import Screen
from primal.engine.camera import OrthographicCamera
from primal.engine.sprite import ColorSprite
from primal.screens.game_screen import GameScreen


class SplashScreen(Screen):
    VP_WIDTH = 1280
    VP_HEIGHT = 720

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time = 4.0

        self.camera = OrthographicCamera(self.canvas, self.VP_WIDTH, self.VP_HEIGHT)
        self.camera.start_region()

        self.bg = ColorSprite(None, pos=(0, 0), size=(self.VP_WIDTH, self.VP_HEIGHT),
                              color=(0, 0, 0, 0))

        self.fg = ColorSprite('banner.png', pos=(0, 0),
                              size=(self.VP_WIDTH, self.VP_HEIGHT), color=(1, 1, 1, 1))

        self.bg.draw(self.canvas)
        self.fg.draw(self.canvas)

        self.camera.end_region()

    def update(self, delta: float):
        self.time -= delta

        if self.time <= 1.5:
            if self.time <= 0:
                self.engine.set_screen(GameScreen())
            else:
                self.fg.set_alpha(self.time / 1.5)
