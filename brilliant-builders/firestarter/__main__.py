import random
from typing import Any

from firestarter.game_engine.engine import Engine
from firestarter.game_engine.object import (
    Duck,
    GenericObject,
    PickUpCoin,
    Platform,
    Player,
    PlayerUiHeart
)

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
        sprite_list = []

        # UI
        self.hearts = PlayerUiHeart(self.assets['hearts'], (0, self.height))
        self.hearts.change_mode(5)
        sprite_list.append(self.hearts)
        # Player
        self.player = Player(self.assets['spritesheet_caveman'], (50, 90))
        self.player.bind(lives=self.update_hearts)
        sprite_list.append(self.player)
        # Platforms and Items, replace this later with a call to load the level
        self.platform_40 = GenericObject('Untitled', (50 + 60 * 5, 20), True, 3, self)
        sprite_list.append(self.platform_40)

        for x in range(-10, 40):
            exec("""self.platform_""" + str(x + 10) + """= Platform(self.assets['Untitled1'],
                (50 + 60 *""" + str(x) + """, 3))""")
            exec("sprite_list.append(self.platform_" + str(x + 10) + ")")

        for x in range(0, 35):
            exec("""self.duck""" + str(x) + """= Duck(self.assets['duck_animation'],
            (1100 - 10 *""" + str(x) + """, 600 - 10 *""" + str(x) + """))""")
            exec("sprite_list.append(self.duck" + str(x) + ")")

        for x in range(0, 20):
            exec("""self.coin""" + str(x) + """= PickUpCoin(self.assets['Untitled'],
            (60 + 50 *""" + str(x) + """, 80 + 40))""")
            exec("sprite_list.append(self.coin" + str(x) + ")")

        self.add_sprites(sprite_list)

#        self.unload_level([self.player, self.hearts, self.platform_1])
        self.load_level(self.levels['testzone'])

        Clock.schedule_interval(lambda dt: self.player.change_mode(self.player.current_mode + 1), 1)

        for x in range(1000):
            img = Image(source='Picture/tree.png',
                        keep_ratio=True,
                        allow_stretch=False,
                        size_hint=(0.5, 0.5),
                        pos_hint={'center_x': random.uniform(0, 1),
                                  'top': random.uniform(0.36, 0.38)})

            self.background.add_widget(img, index=6)

    def update_hearts(self, _: Any, value: int) -> None:
        self.hearts.change_mode(value)
        if value <= 0:
            Clock.schedule_once(lambda *args: self.player.set_lives(5), .5)

    def on_height(self, _: Any, value: int) -> None:
        """Move the hearts to the top left corner."""
        self.hearts.pos = (0, value - 64)

    def update(self, dt: float) -> None:
        for x in range(0, 35):
            exec("self.duck" + str(x) + ".pos[0] = self.duck" + str(x) + ".pos[0] - 2")
            exec("""if self.duck""" + str(x) + """.pos < self.pos:
                    self.duck""" + str(x) + """.pos[0] = 2000 - 10*""" + str(x))

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
        # Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)
        Window.clearcolor = (25 / 255, 51 / 255, 51 / 255, 1)
        self.title = 'FireStarter'
        game = MyGame()
        game.dino_move()
        return game


if __name__ == "__main__":
    Application().run()
