from kivy.app import App
from kivy.clock import Clock
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

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball

    def move(self) -> None:
        self.pos = Vector(*self.velocity) + self.pos


class Dino1(Widget):
    '''Another dinosaur'''
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball

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
        if self.dino.x > self.x + 1300:
            self.dino.pos = -350, -250

        if self.dino1.x > self.x + 1200:
            self.dino1.pos = -350, -250


class StartScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class backgroundApp(App):
    def build(self) -> None:
        game = RootScreen()
        game.dino_move()
        Clock.schedule_interval(game.update, 01.0 / 60.0)
        return game


if __name__ == "__main__":
    backgroundApp().run()
