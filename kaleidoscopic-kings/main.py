# import kivy
# from kivy.lang import Builder
# from kivy.uix.image import Image
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.animation import AnimationTransition
from kivy.uix.carousel import Carousel
from kivy.uix.scatter import Scatter


KEYFRAME = 0


class Trans(AnimationTransition):
    @staticmethod
    def trans(progress):
        global KEYFRAME
        return max(0, min(KEYFRAME, 1))

    def norm(progress):
        return progress + progress


class Swipe(Carousel):
    def __init__(self, **kwargs):
        super(Swipe, self).__init__(**kwargs)
        # self.direction='right'


class Card(Scatter):
    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.keyboard = Window.request_keyboard(None, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        self.trans = Trans.trans

        self.saxis = 0
        self.axis = 0

        self.dir = 0
        self.anim = None

    def on_touch_down(self, touch):
        global KEYFRAME
        KEYFRAME = 0
        self.axis = touch.spos[0]
        self.saxis = touch.spos[0]
        self.anim = None
        self.dir = 0

    def on_touch_move(self, touch):
        global KEYFRAME

        if self.dir == 0:
            self.anim = None

        tmp_dir = 1 if self.axis > self.saxis else -1 if self.axis < self.saxis else 0
        if tmp_dir is not self.dir:
            self.anim = None
        self.dir = tmp_dir
        if self.anim is None:
            if self.dir == -1:
                self.anim = Animation(x=self.x-290,
                                      scale=self.scale + 1,
                                      rotation=90,
                                      transition=self.trans,
                                      duration=1000)
                self.anim.start(self)
            if self.dir == 1:
                self.anim = Animation(x=self.x+290,
                                      scale=self.scale + 1,
                                      rotation=-90,
                                      transition=self.trans,
                                      duration=1000)
                self.anim.start(self)

        difference = self.saxis - touch.spos[0]
        KEYFRAME = abs(difference)

        self.axis = touch.spos[0]

    def on_touch_up(self, touch):
        global KEYFRAME
        KEYFRAME = 0
        self.saxis = 0
        self.axis = 0
        self.dir = 0

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """Moves the image around."""
        global KEYFRAME

        anim = None
        if keycode[1] == 'left':
            anim = Animation(x=self.x-50,
                             transition=self.trans, duration=1000)
        elif keycode[1] == 'right':
            KEYFRAME += 0.1
            # anim = Animation(x=self.x+50)
        elif keycode[1] == 'up':
            anim = Animation(y=self.y+50)
        elif keycode[1] == 'down':
            anim = Animation(y=self.y-50)
        if anim:
            anim.start(self)
        return True


class MainWidget(Widget):
    pass


class myApp(App):

    def build(self):

        return MainWidget()


if __name__ == "__main__":
    myApp().run()
