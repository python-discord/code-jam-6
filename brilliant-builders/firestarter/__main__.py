from firestarter.game_engine.engine import Engine
from firestarter.game_engine.sprite import Player

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window


class MyGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(self.assets['spritesheet_caveman'], (50, 75))
        self.add_sprite(self.player)

        Clock.schedule_interval(lambda dt: self.player.change_mode(self.player.current_mode + 1), 1)

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
