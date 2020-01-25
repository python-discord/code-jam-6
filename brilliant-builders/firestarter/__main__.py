from typing import Any

from firestarter.game_engine.engine import Engine
from firestarter.game_engine.object import GenericObject, PickUpCoin, Platform, Player, PlayerUiHeart

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window


class MyGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # UI
        self.hearts = PlayerUiHeart(self.assets['hearts'], (0, self.height))
        self.hearts.change_mode(5)
        # Player
        self.player = Player(self.assets['spritesheet_caveman'], (50, 90))
        self.player.bind(lives=self.update_hearts)
        # Platforms and Items, replace this later with a call to load the level
        self.platform_01 = Platform(self.assets['Untitled'], (50, 20))
        self.platform_01.change_mode(3)
        self.platform_02 = Platform(self.assets['Untitled'], (50 + 60, 20))
        self.platform_02.change_mode(3)
        self.platform_03 = Platform(self.assets['Untitled'], (50 + 60 * 2, 20))
        self.platform_03.change_mode(3)
        self.platform_04 = Platform(self.assets['Untitled'], (50 + 60 * 3, 20))
        self.platform_04.change_mode(3)
        self.platform_05 = Platform(self.assets['Untitled'], (50 + 60 * 4, 20))
        self.platform_05.change_mode(3)
        self.platform_06 = GenericObject('Untitled', (50 + 60 * 5, 20), True, 3, self)

        self.coin = PickUpCoin(self.assets['Untitled'], (60 + 32 * 5, 80 + 40))
        self.coin.change_mode(2)

        self.add_sprites(
            [self.player,
             self.coin,
             self.platform_01, self.platform_02,
             self.platform_03, self.platform_04,
             self.platform_05, self.platform_06,
             self.hearts
             ]
        )

        self.unload_level([self.player, self.hearts, self.platform_01])
        self.load_level(self.levels['testzone'])

        Clock.schedule_interval(lambda dt: self.player.change_mode(self.player.current_mode + 1), 1)

    def update_hearts(self, _: Any, value: int) -> None:
        self.hearts.change_mode(value)
        if value <= 0:
            Clock.schedule_once(lambda *args: self.player.set_lives(5), .5)

    def on_height(self, _: Any, value: int) -> None:
        """Move the hearts to the top left corner."""
        self.hearts.pos = (0, value - 64)

    def update(self, dt: float) -> None:
        if 'spacebar' in self.pressed_keys and self.player.is_standing:
            self.player.acc_y = 15

        if 'a' in self.pressed_keys:
            self.player.vel_x = -7.5
        if 'd' in self.pressed_keys:
            self.player.vel_x = 7.5


class Application(App):
    """Main application class."""

    def build(self) -> MyGame:
        """Return the root widget."""
        # Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)
        Window.clearcolor = (25 / 255, 51 / 255, 51 / 255, 1)
        self.title = 'FireStarter'
        game = MyGame()
        return game


if __name__ == "__main__":
    Application().run()
