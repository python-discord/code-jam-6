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
    """
    Cannon allows rough simulation of physics, allowing a flat velocity and an angle between 0 and 90 degrees to fire
    a cannonball based on those properties. The input fields allow for user changes to these attributes, with the submit
    buttons finalizing the changes for each.

    1. __init__: creates the background features along with the cannon and cannonball

    2. set_velocity: checks to make sure that the velocity is an integer greater than zero, with no upper limit, then
        converts the string taken from the TextInput in the kv file into an integer and sets it to self.velocity

    3. set_angle: Very similar to set_velocity, but only accepts a number from 0 to 90, and sets the self.angle variable

    4. fire_cannon: sets the position of the cannonball in front of the cannon, adds the velocities of the x and y
        vector based on the input angle and velocity, and schedules a clock object to track each step of its movement

    5. drop: callback used by the fire_cannon clock to apply the simulated effects of gravity by reducing the velocity
        each tick, by 0.98 to adhere to Earth's 9.8m/s/s gravity.
    """
    def __init__(self, **kwargs):
        super(Cannon, self).__init__(**kwargs)
        self.velocity = 10
        self.angle = 30
        
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
