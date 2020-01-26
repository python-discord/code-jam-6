from primal.engine.engine import Engine
from primal.screens.game_screen import GameScreen
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')


class PrimalGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Application(App):
    """Main application class."""

    def build(self):
        """Return the root widget."""
        Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)
        Window.fullscreen = "auto"
        self.title = "Primal"
        game = PrimalGame()
        game.add_screen(GameScreen())

        return game


if __name__ == "__main__":
    print(Window.size)
    Application().run()
