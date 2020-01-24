from kivy.app import App
from kivy.properties import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Rotate
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from math import sin,cos,radians


class Cannon(Widget):
    angle_int_deg = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Cannon, self).__init__(**kwargs)
        self.velocity = 0
        with self.canvas:
            # self.cannon = Rectangle(size=(50, 50))
            self.cannonball = Rectangle(pos=(1000, 1000), size=(5, 5))

    def set_velocity(self, velocity):
        if int(velocity):
            if int(velocity) > 0:
                self.velocity = int(velocity)
                print(self.velocity)

    def set_angle(self,angle):
        print(angle)
        self.angle_int_deg = int(angle)
        self.angle_y = sin(radians(self.angle_int_deg))
        self.angle_x = cos(radians(self.angle_int_deg))

    def fire_cannon(self):
        self.cannonball.pos = (50, 50)
        self.velocity_clock = Clock.schedule_interval(self.drop, 0.1)
        self.velocity_y = self.velocity * self.angle_y
        self.velocity_x = self.velocity * self.angle_x
    def drop(self, dt):

        if self.velocity_x >= 0:
            self.cannonball.pos = (self.cannonball.pos[0] + self.velocity_x, self.cannonball.pos[1] + self.velocity_y)
            self.velocity_y -= 0.98
        else:
            Clock.unschedule(self.velocity_clock)
        if self.cannonball.pos[1] <= 0:
            self.cannonball.pos = (self.cannonball.pos[0], 0)
            Clock.unschedule(self.velocity_clock)

class CannonApp(App):
    def build(self):
        return kv


kv = Builder.load_file("Cannon.kv")
if __name__ == "__main__":
    CannonApp().run()
