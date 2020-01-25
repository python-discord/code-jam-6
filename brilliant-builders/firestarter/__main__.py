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
        sprite_list = []

        self.player = Player(self.assets['spritesheet_caveman'], (50, 90))
        sprite_list.append(self.player)

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
#            self.player.angle = 90

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
