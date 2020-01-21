from firestarter.game_engine.engine import Engine
from firestarter.game_engine.sprite import PickUpCoin, Platform, Player

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty, ObjectProperty, ReferenceListProperty
)
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Dino(Widget):
    '''Widget for the dinosaur'''
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self) -> None:
        self.pos = Vector(*self.velocity) + self.pos


class Dino1(Widget):
    '''Another dinosaur'''
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self) -> None:
        self.pos = Vector(*self.velocity) + self.pos


class RootScreen(ScreenManager):
    '''Screen Transition'''
    dino = ObjectProperty(None)
    dino1 = ObjectProperty(None)

    def dino_move(self, vel: list = (5, 0)) -> None:
        self.dino.velocity = vel
        self.dino1.velocity = vel

    def update(self, dt: float) -> None:
        # call dino.move and other stuff
        self.dino.move()
        self.dino1.move()

        # return the dino to the beginning
        if self.dino.x > self.x + 1900:
            self.dino.pos = -250, -200

        if self.dino1.x > self.x + 1900:
            self.dino1.pos = -300, -230


class StartScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class MyGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(self.assets['spritesheet_caveman'], (50, 90))
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

        self.coin = PickUpCoin(self.assets['Untitled'], (60 + 32 * 5, 80 + 40))
        self.coin.change_mode(2)

        self.add_sprites(
            [self.player,
             self.coin,
             self.platform_01, self.platform_02,
             self.platform_03, self.platform_04,
             self.platform_05
             ]
        )

        Clock.schedule_interval(lambda dt: self.player.change_mode(self.player.current_mode + 1), 1)

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
        Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)
        self.title = 'FireStarter'
        game = MyGame()
        screen = RootScreen()
        screen.dino_move()
        Clock.schedule_interval(screen.update, 0 / 60.0)
        return game


if __name__ == "__main__":
    Application().run()
