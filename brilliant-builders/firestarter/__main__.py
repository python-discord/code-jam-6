from firestarter.game_engine.engine import Engine
from firestarter.game_engine.sprite import PickUpCoin, Platform, Player

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window


class MyGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(self.assets['spritesheet_caveman'], (50, 90))
        self.platform_01 = Platform(self.assets['Untitled'], (50, 20))
        self.platform_02 = Platform(self.assets['Untitled'], (50 + 32, 20))
        self.platform_03 = Platform(self.assets['Untitled'], (50 + 32 * 2, 20))

        self.platform_04 = Platform(self.assets['Untitled'], (60 + 32 * 4, 80))
        self.platform_05 = Platform(self.assets['Untitled'], (60 + 32 * 5, 80))
        self.platform_06 = Platform(self.assets['Untitled'], (60 + 32 * 6, 80))

        self.coin = PickUpCoin(self.assets['Untitled'], (60 + 32 * 5, 80 + 40))
        self.coin.change_mode(2)

        self.add_sprites([self.platform_01, self.platform_02, self.platform_03,
                          self.platform_04, self.platform_05, self.platform_06])
        for s in self.sprites:
            s.change_mode(3)
        self.add_sprite(self.player)
        self.add_sprite(self.coin)

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
