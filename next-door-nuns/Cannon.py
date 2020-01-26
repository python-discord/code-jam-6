from kivy.app import App
from kivy.properties import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Rotate, context_instructions
from kivy.properties import NumericProperty
from math import sin, cos, radians
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import random


class Cannon(Widget):
    angle_int_deg = NumericProperty(50)
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
        self.velocity = 0
        self.velocity_clock = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 0
        self.x_collide = False
        self.y_collide = False
        self.x_rand = 0
        self.y_rand = 0
        random.seed()
        with self.canvas:
            self.sky = Rectangle(size=(2000, 1000), source="Back_Drop.png")
            self.grass = Rectangle(size=(2000, 100), source="Grass.png")
            self.target = Rectangle(size=(35, 35), pos=(400, 0), source="python_discord_logo.png")
            self.wheel = Rectangle(size=(35, 35), pos=(20, 0), source="Wheel.png")

            # Draws the cannon and binds rotation object to it for changing in set_angle()
            self.canvas.before
            context_instructions.PushMatrix()
            self.rotate = Rotate(origin=(42.5, 12.5), angle=self.angle)
            self.cannon = Rectangle(size=(50, 15), pos=(35, 10), source="cannon.png")
            context_instructions.PopMatrix()
            self.canvas.after

            self.cannonball = Rectangle(pos=(1000, 1000), size=(10, 10), source="Cannon_Ball.png")

    def set_velocity(self, velocity):
        """ Sets the velocity for the projectile """
        if int(velocity):
            if int(velocity) > 0:
                self.velocity = int(velocity)
                print(self.velocity)


    def set_angle(self, angle):
        """ Sets the angle of the cannon and updates the rotation"""
        # self.angle_int_deg = int(angle)
        if int(angle):
            if -1 < int(angle) <= 90:
                self.angle = int(angle)
                self.rotate.angle = self.angle

    def fire_cannon(self):
        self.cannonball.pos = (int(self.cannon.pos[0] + cos(radians(self.angle))
                               * self.cannon.size[0] / 2),
                                int(self.cannon.pos[1] + sin(radians(self.angle))
                               * self.cannon.size[1] / 2))
        self.velocity_clock = Clock.schedule_interval(self.drop, 0.1)
        self.velocity_y = self.velocity * (self.angle / 90)
        self.velocity_x = self.velocity - self.velocity_y

    def drop(self, dt):
        """Updates the position of the cannonball and detects collision
        with target"""
        if self.velocity_x >= 0:
            self.cannonball.pos = (self.cannonball.pos[0] + self.velocity_x,
                               self.cannonball.pos[1] + self.velocity_y)
            self.velocity_y -= 0.98

        # Checks for X position collision
        if (self.cannonball.pos[0] < (self.target.pos[0] + self.target.size[0])) and \
                (self.cannonball.pos[0] > (self.target.pos[0])):
            self.x_collide = True

        else:
            self.x_collide = False

        # Checks for Y position collision
        if (self.cannonball.pos[1] < (self.target.pos[1] + self.target.size[1])) and \
                (self.cannonball.pos[1] > (self.target.pos[1])):
            self.y_collide = True
        else:
            self.y_collide = False

        # If X and Y collision are both true, collision with target
        if self.x_collide is True and self.y_collide is True:
            content = Button(text='Press to Try Again')
            self.P = Popup(title="TARGET HIT!!!!", title_align='center',
                           title_size=40, title_color=[1, 0, 0, 1], content=content,
                           size_hint=(None, None), size=(400, 400), auto_dismiss=False)
            content.bind(on_press=self.P.dismiss)
            self.P.open()

            # Generate random number for coordinate of next target
            self.x_rand = random.randint(20, 600)
            self.y_rand = random.randint(0, 400)
            self.target.pos = (self.x_rand, self.y_rand)

        if self.cannonball.pos[1] <= 0:
            self.cannonball.pos = (self.cannonball.pos[0], 0)
            Clock.unschedule(self.velocity_clock)


class CannonApp(App):
    def build(self):
        return kv


kv = Builder.load_file("Cannon.kv")
if __name__ == "__main__":
    CannonApp().run()
