import kivy
kivy.require('1.11.1') # noqa

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Mesh, Rotate

import math
import random
from typing import List


class Sky(Widget):

    def __init__(self, **kwargs):
        super(Sky, self).__init__(**kwargs)

        self.sprite = Image(source="assets/images/sky.png")
        self.sprite.size = self.sprite.texture_size
        self.sprite.pos = (0, 0)
        self.add_widget(self.sprite)


class Sun(Widget):

    def __init__(self, **kwargs):
        super(Sun, self).__init__(**kwargs)

        self.anim_interval = 1/2
        self.anim_interval_tracker = 0
        self.frame_id = 0
        self.sprite_path = "atlas://assets/images/sun_anim/"
        self.sprite = Image(
            source=self.sprite_path + f"sun-{self.frame_id}")

        self.sprite.size = self.sprite.texture_size
        self.sprite.pos = (650, 530)
        self.add_widget(self.sprite)

    def update(self, dt):
        self.anim_interval_tracker += dt
        if(self.anim_interval_tracker >= self.anim_interval):
            self.anim_interval_tracker = 0
            self.frame_id += 1
            if self.frame_id > 1:
                self.frame_id = 0

            self.sprite.source = self.sprite_path + f"sun-{self.frame_id}"


class FlockOfBirds(Widget):

    def __init__(self, **kwargs):
        super(FlockOfBirds, self).__init__(**kwargs)

        self.anim_interval = 1/5
        self.anim_interval_tracker = 0
        self.frame_id = 0
        self.sprite_path = "atlas://assets/images/bird_anim/"
        self.sprite = Image(
            source=self.sprite_path + f"bird-{self.frame_id}")

        self.sprite.size = self.sprite.texture_size
        self.sprite.pos = (1200, 400)
        self.add_widget(self.sprite)

    def update(self, dt):
        self.anim_interval_tracker += dt
        if(self.anim_interval_tracker >= self.anim_interval):
            self.anim_interval_tracker = 0

            # Move the flock of birds ahead
            self.sprite.pos[0] -= 10
            if(self.sprite.pos[0] <= -self.sprite.size[0]):
                self.sprite.pos[0] = random.randint(1200, 4800)

            self.frame_id += 1
            if self.frame_id > 1:
                self.frame_id = 0

            self.sprite.source = self.sprite_path + f"bird-{self.frame_id}"


class Island(Widget):

    def __init__(self, **kwargs):
        super(Island, self).__init__(**kwargs)

        self.sprite = Image(source="assets/images/island.png")
        self.sprite.size = self.sprite.texture_size
        self.sprite.pos = (0, 0)
        self.add_widget(self.sprite)


class Sea(Widget):

    def __init__(self, **kwargs):
        super(Sea, self).__init__(**kwargs)

        self.anim_interval = 1/5
        self.anim_interval_tracker = 0
        self.frame_id = 0
        self.sprite_path = "atlas://assets/images/sea_anim/"
        self.sprite = Image(
            source=self.sprite_path + f"sea-{self.frame_id}")
        self.sprite.size = self.sprite.texture_size
        self.sprite.pos = (0, 0)
        self.add_widget(self.sprite)

    def update(self, dt):
        self.anim_interval_tracker += dt
        if(self.anim_interval_tracker >= self.anim_interval):
            self.anim_interval_tracker = 0
            self.frame_id += 1
            if self.frame_id > 1:
                self.frame_id = 0

            self.sprite.source = self.sprite_path + f"sea-{self.frame_id}"


class MirrorCannon(Widget):

    def __init__(self, **kwargs):
        super(MirrorCannon, self).__init__(**kwargs)

        self._angle = 75

        # Mirror centre position with respect to the image
        self._mirror_center = (97, 78)
        self.mirror_diameter = 80

        self.sprite_path = "atlas://assets/images/mirror_cannon/"
        self.sprite = Image(
            source=self.sprite_path + f"angle-{self._angle}")
        self.sprite.size = self.sprite.texture_size
        self.sprite.pos = (150, 260)
        self.add_widget(self.sprite)


    # A property which returns mirror centre position w.r.t the window origin
    @property
    def mirror_center(self):
        return (self.sprite.pos[0]+self._mirror_center[0],
                self.sprite.pos[1]+self._mirror_center[1])

    @property
    def mirror_axis_line(self):
        x1, y1 = self.mirror_center
        x2 = x1 + round( 0.5*self.mirror_diameter*math.cos(math.radians(self._angle)))
        y2 = y1 + round(0.5*self.mirror_diameter*math.sin(math.radians(self._angle)))
        x3 = x1 - round( 0.5*self.mirror_diameter*math.cos(math.radians(self._angle)))
        y3 = y1 - round(0.5*self.mirror_diameter*math.sin(math.radians(self._angle)))
        return (x3,y3,x2,y2)

    @property
    def angle(self):
        return self._angle

    def increase_angle(self):
        self._angle += 15
        if self._angle >= 150:
            self._angle = 150

    def decrease_angle(self):
        self._angle -= 15
        if self._angle <= 75:
            self._angle = 75

    def update(self, dt):
        self.sprite.source = self.sprite_path + f"angle-{self._angle}"


class LightRays(Mesh):

    def __init__(self, point, mirror, **kwargs):
        super(LightRays, self).__init__(**kwargs)
        self.color = Color(01.0, 0.98, 0.1, 0.65)
        self.vertices = []
        self.indices = []
        self.mode = 'traingle_fan'
        self.point = point
        self.mirror = mirror

    def increase_height(self):
        x, y = self.point
        y += 50
        if(y > 300):
           y = 300
        self.point = (x,y)

    def decrease_height(self):
        x, y = self.point
        y -=50
        if(y < 50):
           y = 50
        self.point = (x,y)

    def trace(self, mirror):
        # Compute the vertices for sunray mesh 
        x3, y3 = self.point
        self.mirror = mirror
        x1, y1, x2, y2 = self.mirror

        self.indices = [0, 1, 2]
        self.vertices = []

        # vertices for the incident sun rays
        self.vertices.extend([x1, y1, x2, y2])
        self.vertices.extend([x2, y2, x3, y3])
        self.vertices.extend([x3, y3, x1, y1])

class GameWorld(Widget):

    def __init__(self, **kwargs):
        super(GameWorld, self).__init__(**kwargs)

        self.add_widget(Sky())
        self.sun = Sun()
        self.add_widget(self.sun)
        self.birds = FlockOfBirds()
        self.add_widget(self.birds)

        self.sea = Sea()
        self.add_widget(self.sea)
        self.add_widget(Island())
        self.mirror_cannon = MirrorCannon()
        self.add_widget(self.mirror_cannon)

        # create sun_rays
        self.sun_rays = LightRays(
            point=(
                self.sun.sprite.pos[0]+100, self.sun.sprite.pos[1]+100),
            mirror=self.mirror_cannon.mirror_axis_line)
        self.canvas.add(self.sun_rays.color)
        self.canvas.add(self.sun_rays)

        # create death_rays
        self.death_rays = LightRays(
            point=(900, 50),
            mirror=self.mirror_cannon.mirror_axis_line)
        self.canvas.add(self.death_rays.color)
        self.canvas.add(self.death_rays)

        # Set update rate of the game to 60 times per second
        Clock.schedule_interval(self.update, 1/60)

        # Initialize the Keybaord for game input
        self.getKeyboard()

    def getKeyboard(self):
        self._keybaord = Window.request_keyboard(
            self._keyboard_closed, self, 'text')

        self._keybaord.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keybaord, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.mirror_cannon.increase_angle()
            self.death_rays.increase_height()
        if keycode[1] == 's':
            self.mirror_cannon.decrease_angle()
            self.death_rays.decrease_height()


    def update(self, dt):
        self.mirror_cannon.update(dt)
        self.sea.update(dt)
        self.sun.update(dt)
        self.birds.update(dt)

        # Trace the light rays from the sun to the mirror
        self.sun_rays.trace(mirror=self.mirror_cannon.mirror_axis_line)

        # Trace the death rays from the mirror and focus to a point
        self.death_rays.trace(mirror=self.mirror_cannon.mirror_axis_line)


class GameApp(App):

    def build(self):
        Window.minimum_height = 800
        Window.minimum_width = 1200
        return GameWorld(size=Window.size)


if __name__ == "__main__":
    GameApp().run()
