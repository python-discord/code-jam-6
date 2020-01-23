import random
import kivy
kivy.require('1.11.1') # noqa

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Line


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
        self.sprite.pos = (1200, 500)
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
        self.sprite_path = "atlas://assets/images/mirror_cannon/"
        self.sprite = Image(
            source=self.sprite_path + f"angle-{self._angle}")
        self.sprite.size = self.sprite.texture_size
        self.sprite.pos = (150, 260)
        self.add_widget(self.sprite)

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


def SunRays(Widget):

    def __init__(self, **kwargs):
        super(SunRays, self).__init__(**kwargs)
        pass


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
        Clock.schedule_interval(self.update, 1/60)
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

        if keycode[1] == 's':
            self.mirror_cannon.decrease_angle()

    def update(self, dt):
        self.mirror_cannon.update(dt)
        self.sea.update(dt)
        self.sun.update(dt)
        self.birds.update(dt)

        x1, y1 = self.sun.sprite.pos[0]+100, self.sun.sprite.pos[1]+100
        x2, y2 = self.mirror_cannon.sprite.pos[0]+97, self.mirror_cannon.sprite.pos[1]+80+80/2
        x3, y3 = self.mirror_cannon.sprite.pos[0]+97, self.mirror_cannon.sprite.pos[1]+78-80/2

        self.canvas.add(Color(1, 1, 0, 0.125))
        self.canvas.add(Line(points=[x1, y1, x2, y2, x3, y3, x1, y1], width=1.5, closed=True))


class GameApp(App):

    def build(self):
        Window.minimum_height = 800
        Window.minimum_width = 1200
        return GameWorld(size=Window.size)


if __name__ == "__main__":
    GameApp().run()
