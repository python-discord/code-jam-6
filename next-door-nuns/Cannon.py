from kivy.app import App
from kivy.properties import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Rotate, Color,context_instructions
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from math import sin,cos,radians
from kivy.animation import Animation

class Cannon(Widget):
    angle_int_deg= NumericProperty(50)
    def __init__(self, **kwargs):
        super(Cannon, self).__init__(**kwargs)
        self.velocity = 0
        self.angle = 0
        with self.canvas:
            self.sky = Rectangle(size=(2000, 1000), source="Back_Drop.png")
            self.grass = Rectangle(size=(2000, 100), source="Grass.png")

            self.wheel = Rectangle(size=(35, 35), pos=(20, 0), source="Wheel.png")

            self.canvas.before
            context_instructions.PushMatrix()
            self.rotate = Rotate(origin=(35,12.5), angle=self.angle)
            self.cannon = Rectangle(size=(50, 15), pos=(35, 10), source="cannon.png")
            #self.cannon = Rectangle(size=(50, 15), pos=(35, 15))
            context_instructions.PopMatrix()
            self.canvas.after


            self.cannonball = Rectangle(pos=(1000, 1000), size=(10, 10), source="Cannon_Ball.png")

    def set_velocity(self, velocity):
        if int(velocity):
            if int(velocity) > 0:
                self.velocity = int(velocity)
                print(self.velocity)

    def set_angle(self, angle):
        # self.angle_int_deg = int(angle)
        if int(angle):
            if -1 < int(angle) <= 90:
                self.angle = int(angle)
                self.rotate.angle = self.angle



    def rot_animation(self, instance):
        self.animation = Animation(angle=self.angle, duration=1)
        self.animation += Animation(angle=self.angle + 10, duration=1)
        self.animation.start(self.cannon)

    def fire_cannon(self):
        # self.cannonball.pos = (self.cannon.pos[0] + self.cannon.size[0], self.cannon.pos[1] + self.cannon.size[1]/2)
        self.cannonball.pos = (int(self.cannon.pos[0]+cos(radians(self.angle))*self.cannon.size[0]),
                               int(self.cannon.pos[1] + sin(radians(self.angle))*self.cannon.size[1]))
        print(self.cannonball.pos)
        self.velocity_clock = Clock.schedule_interval(self.drop, 0.1)
        self.velocity_y = self.velocity * (self.angle / 90)
        self.velocity_x = self.velocity - self.velocity_y

    def drop(self, dt):

        if self.velocity_x >= 0:
            self.cannonball.pos = (self.cannonball.pos[0] + self.velocity_x, self.cannonball.pos[1] + self.velocity_y)
            self.velocity_y -= 0.98
            

        else:
            Clock.unschedule(self.velocity_clock)
        if self.cannonball.pos[1] <= 0:
            self.cannonball.pos = (self.cannonball.pos[0], 0)
            Clock.unschedule(self.velocity_clock)

class Target(Widget):
    pass
class CannonApp(App):
    def build(self):
        return kv


kv = Builder.load_file("Cannon.kv")
if __name__ == "__main__":
    CannonApp().run()
