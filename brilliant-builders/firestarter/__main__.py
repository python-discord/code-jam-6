from kivy.app import App
from kivy.core.window import Window

from firestarter.game_engine.engine import Engine
from firestarter.game_engine.sprite import Player


class MyGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player('Bob-01.jpg', (50, 50))

        self.add_sprite(self.player)

    def update(self, dt: float) -> None:
        if 'spacebar' in self.pressed_keys:
            self.player.vel_y = 25

        if 'a' in self.pressed_keys:
            self.player.vel_x = -10
        if 'd' in self.pressed_keys:
            self.player.vel_x = 10


class Application(App):
    """Main application class."""

    def build(self) -> MyGame:
        """Return the root widget."""
        Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)
        self.title = 'FireStarter'
        game = MyGame()
        return game


if __name__ == "__main__":
    Application().run()
