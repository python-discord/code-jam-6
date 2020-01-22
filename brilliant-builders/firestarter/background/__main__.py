import random

from firestarter.game_engine.engine import Engine
from firestarter.game_engine.sprite import Duck, PickUpCoin, Platform, Player

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty, ObjectProperty, ReferenceListProperty
)
from kivy.uix.image import Image
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
        self.duck = Duck(self.assets['duck_animation'], (800, 500))
        self.duck1 = Duck(self.assets['duck_animation'], (1100, 400))
        self.duck2 = Duck(self.assets['duck_animation'], (300, 600))
        self.duck3 = Duck(self.assets['duck_animation'], (900, 300))

        self.coin = PickUpCoin(self.assets['Untitled'], (60 + 32 * 5, 80 + 40))
        self.coin.change_mode(2)

        self.add_sprites(
            [self.player,
             self.coin,
             self.duck,
             self.duck1,
             self.duck2,
             self.duck3,
             self.platform_01, self.platform_02,
             self.platform_03, self.platform_04,
             self.platform_05
             ]
        )

        Clock.schedule_interval(lambda dt: self.player.change_mode(self.player.current_mode + 1), 1)

        for x in range(20):
            img = Image(source='Picture/tree.png',
                        keep_ratio=True,
                        allow_stretch=False,
                        size_hint=(0.2, 0.25),
                        pos_hint={'center_x': random.uniform(0, 1),
                                  'top': random.uniform(0.26, 0.24)})

            self.background.add_widget(img, index=6)

    def update(self, dt: float) -> None:
        self.duck.pos[0] = self.duck.pos[0] - 3
        self.duck1.pos[0] = self.duck1.pos[0] - 3
        self.duck2.pos[0] = self.duck2.pos[0] - 3
        self.duck3.pos[0] = self.duck3.pos[0] - 3

        if self.duck.pos < self.pos:
            self.duck.pos[0] = 1400

        if self.duck1.pos < self.pos:
            self.duck1.pos[0] = 1600

        if self.duck2.pos < self.pos:
            self.duck2.pos[0] = 1700

        if self.duck3.pos < self.pos:
            self.duck3.pos[0] = 1650

        if 'spacebar' in self.pressed_keys and self.player.is_standing:
            self.player.acc_y = 15

        if 'a' in self.pressed_keys:
            self.player.vel_x = -7.5

        if 'd' in self.pressed_keys:
            self.player.vel_x = 7.5

    dino = ObjectProperty(None)
    dino1 = ObjectProperty(None)

    def dino_move(self, vel: tuple = (5, 0)) -> None:
        self.dino.velocity = vel
        self.dino1.velocity = (vel[0] - 1, vel[1])

    def dino_update(self, dt: float) -> None:
        # call dino.move and other stuff
        self.dino.move()
        self.dino1.move()

        # return the dino to the beginning
        if self.dino.x > self.x + 2200:
            self.dino.pos = -300, -10

        if self.dino1.x > self.x + 1850:
            self.dino1.pos = -450, -20


class Application(App):
    """Main application class."""
    def build(self) -> MyGame:
        """Return the root widget."""
        Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)
        Window.fullscreen = 'auto'
        self.title = 'FireStarter'
        game = MyGame()
        game.dino_move()
        return game


if __name__ == "__main__":
    Application().run()
