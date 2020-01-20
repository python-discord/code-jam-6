from kivy.app import App

from src.core.game_loop import GameLoop
from src.core.screen_manager import ScreenManager


class Game(App):
    def __init__(self, loop: GameLoop, screen_manager: ScreenManager, **kwargs):
        super().__init__(**kwargs)

        self.loop = loop
        self.screen_manager = screen_manager

        self.loop.set_callback(self.loop_callback)

    def build(self):
        return self.screen_manager

    def loop_callback(self, delta):
        if self.screen_manager.current is not None:
            self.screen_manager.current.update(delta)
            self.screen_manager.current.render_screen(delta)
