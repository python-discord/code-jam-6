# import kivy
# from kivy.lang import Builder
# from kivy.uix.image import Image
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import AsyncImage
# from kivy.core.window import Window
# from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
import frontend.animation_controller as ac


class Rotater(Scatter):
    def __init__(self, **kwargs):
        super(Rotater, self).__init__(**kwargs)
        self.size = (800, 800)
        self.rotation = 0

        self.init_x = self.x
        self.init_y = self.y
        self.trans = ac.Trans.trans

        self.saxis = 0
        self.axis = 0

        self.dir = 0
        self.anim = None

    def on_touch_down(self, touch):
        ac.KEYFRAME = 0
        self.axis = touch.spos[0]
        self.saxis = touch.spos[0]
        self.anim = None
        self.dir = 0

    def on_touch_move(self, touch):
        if self.dir == 0:
            self.anim = None

        tmp_dir = 1 if self.axis > self.saxis else -1 if self.axis < self.saxis else 0
        if tmp_dir is not self.dir:
            self.anim = None
        self.dir = tmp_dir
        if self.anim is None:
            if self.dir == -1:
                self.anim = Animation(x=self.init_x-1500,
                                      rotation=25,
                                      transition=self.trans,
                                      duration=1000)
                self.anim.start(self)
            if self.dir == 1:
                self.anim = Animation(x=self.init_y+1500,
                                      rotation=-25,
                                      transition=self.trans,
                                      duration=1000)
                self.anim.start(self)

        difference = self.saxis - touch.spos[0]
        ac.KEYFRAME = abs(difference)

        self.axis = touch.spos[0]

    def on_touch_up(self, touch):
        ac.KEYFRAME = 0
        self.saxis = 0
        self.axis = 0
        self.dir = 0
        if self.anim:
            self.anim.stop(self)


class SwipeCard(FloatLayout):
    def __init__(self, **kwargs):
        super(SwipeCard, self).__init__(**kwargs)
        self.size = (800, 800)

    # def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     """Moves the image around."""

    #     anim = None
    #     if keycode[1] == 'left':
    #         anim = Animation(x=self.x-50,
    #                          transition=self.trans, duration=1000)
    #     elif keycode[1] == 'right':
    #         ac.KEYFRAME += 0.1
    #         # anim = Animation(x=self.x+50)
    #     elif keycode[1] == 'up':
    #         anim = Animation(y=self.y+50)
    #     elif keycode[1] == 'down':
    #         anim = Animation(y=self.y-50)
    #     if anim:
    #         anim.start(self)
    #     return True
