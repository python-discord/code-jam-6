from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.image import Image
#from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle
#from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock

class Dino(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class RootScreen(ScreenManager):
    dino = ObjectProperty(None)

    def dino_move(self, vel=(3, 0)):
        self.dino.velocity = vel

    def update(self, dt):
        # call dino.move and other stuff
        self.dino.move()

        # return the dino to the beginning
        if self.dino.x > self.x + 1300:
            self.dino.pos = -350, -250

class StartScreen(Screen):
    pass

class GameScreen(Screen):
    pass


class backgroundApp(App):
    def build(self):
        game = RootScreen()
        game.dino_move()
        Clock.schedule_interval(game.update, 60.0/60.0)
        return game

if __name__ == "__main__":
    backgroundApp().run()
