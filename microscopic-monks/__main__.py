from primal.engine.engine import Engine
from primal.screens.splash_screen import SplashScreen
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
        Window.clearcolor = (0, 0, 0, 1)
        # Window.fullscreen = "auto"
        self.title = "Primal"
        game = PrimalGame()
        game.set_screen(SplashScreen())

        return game


if __name__ == "__main__":
    print(Window.size)
    Application().run()
