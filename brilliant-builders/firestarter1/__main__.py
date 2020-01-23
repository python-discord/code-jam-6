import random

from firestarter1.game_engine.engine import Engine
from firestarter1.game_engine.sprite import Duck, PickUpCoin, Platform, Player

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
        self.platform_00 = Platform(self.assets['Untitled1'], (-10, 3))
        self.platform_00.change_mode(3)
        self.platform_01 = Platform(self.assets['Untitled1'], (50, 3))
        self.platform_01.change_mode(3)
        self.platform_02 = Platform(self.assets['Untitled1'], (50 + 60, 3))
        self.platform_02.change_mode(3)
        self.platform_03 = Platform(self.assets['Untitled1'], (50 + 60 * 2, 3))
        self.platform_03.change_mode(3)
        self.platform_04 = Platform(self.assets['Untitled1'], (50 + 60 * 3, 3))
        self.platform_04.change_mode(3)
        self.platform_05 = Platform(self.assets['Untitled1'], (50 + 60 * 4, 3))
        self.platform_05.change_mode(3)
        self.platform_06 = Platform(self.assets['Untitled1'], (50 + 60 * 5, 3))
        self.platform_06.change_mode(3)
        self.platform_07 = Platform(self.assets['Untitled1'], (50 + 60 * 6, 3))
        self.platform_07.change_mode(3)
        self.platform_08 = Platform(self.assets['Untitled1'], (50 + 60 * 7, 3))
        self.platform_08.change_mode(3)
        self.platform_09 = Platform(self.assets['Untitled1'], (50 + 60 * 8, 3))
        self.platform_09.change_mode(3)
        self.platform_10 = Platform(self.assets['Untitled1'], (50 + 60 * 9, 3))
        self.platform_10.change_mode(3)
        self.platform_11 = Platform(self.assets['Untitled1'], (50 + 60 * 10, 3))
        self.platform_11.change_mode(3)
        self.platform_12 = Platform(self.assets['Untitled1'], (50 + 60 * 11, 3))
        self.platform_12.change_mode(3)
        self.platform_13 = Platform(self.assets['Untitled1'], (50 + 60 * 12, 3))
        self.platform_13.change_mode(3)
        self.platform_14 = Platform(self.assets['Untitled1'], (50 + 60 * 13, 3))
        self.platform_14.change_mode(3)
        self.platform_15 = Platform(self.assets['Untitled1'], (50 + 60 * 14, 3))
        self.platform_15.change_mode(3)
        self.platform_16 = Platform(self.assets['Untitled1'], (50 + 60 * 15, 3))
        self.platform_16.change_mode(3)
        self.platform_17 = Platform(self.assets['Untitled1'], (50 + 60 * 16, 3))
        self.platform_17.change_mode(3)
        self.platform_18 = Platform(self.assets['Untitled1'], (50 + 60 * 17, 3))
        self.platform_18.change_mode(3)
        self.platform_19 = Platform(self.assets['Untitled1'], (50 + 60 * 18, 3))
        self.platform_19.change_mode(3)
        self.platform_20 = Platform(self.assets['Untitled1'], (50 + 60 * 19, 3))
        self.platform_20.change_mode(3)
        self.platform_21 = Platform(self.assets['Untitled1'], (50 + 60 * 20, 3))
        self.platform_21.change_mode(3)
        self.platform_22 = Platform(self.assets['Untitled1'], (50 + 60 * 21, 3))
        self.platform_22.change_mode(3)
        self.platform_23 = Platform(self.assets['Untitled1'], (50 + 60 * 22, 3))
        self.platform_23.change_mode(3)
        self.platform_24 = Platform(self.assets['Untitled1'], (50 + 60 * 23, 3))
        self.platform_24.change_mode(3)
        self.platform_25 = Platform(self.assets['Untitled1'], (50 + 60 * 24, 3))
        self.platform_25.change_mode(3)
        self.platform_26 = Platform(self.assets['Untitled1'], (50 + 60 * 25, 3))
        self.platform_26.change_mode(3)
        self.platform_27 = Platform(self.assets['Untitled1'], (50 + 60 * 26, 3))
        self.platform_27.change_mode(3)
        self.platform_28 = Platform(self.assets['Untitled1'], (50 + 60 * 27, 3))
        self.platform_28.change_mode(3)
        self.platform_29 = Platform(self.assets['Untitled1'], (50 + 60 * 28, 3))
        self.platform_29.change_mode(3)
        self.platform_30 = Platform(self.assets['Untitled1'], (50 + 60 * 29, 3))
        self.platform_30.change_mode(3)
        self.platform_31 = Platform(self.assets['Untitled1'], (50 + 60 * 30, 3))
        self.platform_31.change_mode(3)
        self.platform_32 = Platform(self.assets['Untitled1'], (50 + 60 * 31, 3))
        self.platform_32.change_mode(3)
        self.platform_33 = Platform(self.assets['Untitled1'], (50 + 60 * 32, 3))
        self.platform_33.change_mode(3)
        self.platform_34 = Platform(self.assets['Untitled1'], (50 + 60 * 33, 3))
        self.platform_34.change_mode(3)
        self.platform_35 = Platform(self.assets['Untitled1'], (50 + 60 * 34, 3))
        self.platform_35.change_mode(3)
        self.platform_36 = Platform(self.assets['Untitled1'], (50 + 60 * 35, 3))
        self.platform_36.change_mode(3)
        self.platform_37 = Platform(self.assets['Untitled1'], (50 + 60 * 36, 3))
        self.platform_37.change_mode(3)
        self.platform_38 = Platform(self.assets['Untitled1'], (50 + 60 * 37, 3))
        self.platform_38.change_mode(3)
        self.platform_39 = Platform(self.assets['Untitled1'], (50 + 60 * 38, 3))
        self.platform_39.change_mode(3)
        self.platform_40 = Platform(self.assets['Untitled1'], (50 + 60 * 39, 3))
        self.platform_40.change_mode(3)
        self.platform_41 = Platform(self.assets['Untitled1'], (50 + 60 * 40, 3))
        self.platform_41.change_mode(3)

        self.duck = Duck(self.assets['duck_animation'], (800, 500))
        self.duck1 = Duck(self.assets['duck_animation'], (1100, 400))
        self.duck2 = Duck(self.assets['duck_animation'], (300, 600))
        self.duck3 = Duck(self.assets['duck_animation'], (900, 300))

        self.coin = PickUpCoin(self.assets['Untitled'], (60 + 32 * 5, 80 + 40))
        self.coin1 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 6, 80 + 40))
        self.coin2 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 7, 80 + 40))
        self.coin3 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 8, 80 + 40))
        self.coin4 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 9, 80 + 40))
        self.coin5 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 10, 80 + 40))
        self.coin6 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 11, 80 + 40))
        self.coin7 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 12, 80 + 40))
        self.coin8 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 13, 80 + 40))
        self.coin9 = PickUpCoin(self.assets['Untitled'], (60 + 32 * 14, 80 + 40))

        self.add_sprites(
            [self.player,
             self.coin, self.coin1,
             self.coin2, self.coin3,
             self.coin4, self.coin5,
             self.coin6, self.coin7,
             self.coin8, self.coin9,
             self.duck,
             self.duck1,
             self.duck2,
             self.duck3,
             self.platform_00,
             self.platform_01, self.platform_02,
             self.platform_03, self.platform_04,
             self.platform_05, self.platform_06,
             self.platform_07, self.platform_08,
             self.platform_09, self.platform_10,
             self.platform_11, self.platform_12,
             self.platform_13, self.platform_14,
             self.platform_15, self.platform_16,
             self.platform_17, self.platform_18,
             self.platform_19, self.platform_20,
             self.platform_21, self.platform_22,
             self.platform_23, self.platform_24,
             self.platform_25, self.platform_26,
             self.platform_27, self.platform_28,
             self.platform_29, self.platform_30,
             self.platform_31, self.platform_32,
             self.platform_33, self.platform_34,
             self.platform_35, self.platform_36,
             self.platform_37, self.platform_38,
             self.platform_39, self.platform_40,
             self.platform_41

             ]
        )

        Clock.schedule_interval(lambda dt: self.player.change_mode(self.player.current_mode + 1), 1)

        for x in range(1000):
            img = Image(source='Picture/tree.png',
                        keep_ratio=True,
                        allow_stretch=False,
                        size_hint=(0.5, 0.5),
                        pos_hint={'center_x': random.uniform(0, 1),
                                  'top': random.uniform(0.36, 0.38)})

            self.background.add_widget(img, index=6)

    def update(self, dt: float) -> None:
        self.duck.pos[0] = self.duck.pos[0] - 2
        self.duck1.pos[0] = self.duck1.pos[0] - 2
        self.duck2.pos[0] = self.duck2.pos[0] - 2
        self.duck3.pos[0] = self.duck3.pos[0] - 2

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
