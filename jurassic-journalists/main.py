'''Jurassic Journalists'''
from io import BytesIO
from kivy.config import Config
Config.set('graphics', 'resizable', False) # noqa
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.gesturesurface import GestureSurface
# from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, NumericProperty # noqa
from kivy.graphics import (
    Canvas, Translate, Fbo, ClearColor, ClearBuffers, Scale)
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from PIL import ImageDraw
from PIL import Image as Im
from time import sleep
from threading import Thread

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = Window.size
if SCREEN_HEIGHT / SCREEN_WIDTH < 1.5:
    SCREEN_WIDTH = 540
    SCREEN_HEIGHT = 720
STARTING_X = 50
STARTING_Y = 50
PAPER_WIDTH = SCREEN_WIDTH * .7 - STARTING_X
PAPER_HEIGHT = SCREEN_WIDTH


class MainScreen(ScreenManager):
    ''' ScreenManager '''


class RoomScreen(Screen):
    ''' Screen One '''


class PhoneScreen(Screen):
    ''' Screen Two '''


class TypeWriter(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.keyboard.bind(on_key_down=self._key_down)
    def _key_down(self, keyboard, keycode, *args):
        punctuation = {';': 'semicolon', ':': 'colon', '#': 'enter', ' ': 'spacebar'}
        key = keycode[1]
        if key in self.ids:
            self.ids[key].trigger_action()
        elif key in punctuation:
            if key == ';':
                if args[0] == 'shift':
                    key = ':'
            self.ids[punctuation[key]].trigger_action()
        else:
            return False

    def _keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._key_down)
        self.keyboard = None


class AutoButton(Button):
    def on_release(self):
        # Clock.schedule_once(Thread(None, self._auto_text).run)
        # not sure if using Clock would work / be better here
        Thread(None, self._auto_text).start()

    def _auto_text(self):
        for i in 'all work and no play makes joe a dull boy ':
            # there's got to be a shorter way to get to the method needed
            self.parent.parent.parent.parent._key_down(self, ('auto', i))
            sleep(.1)


class TypeWriterButton(Button):
    sound = SoundLoader.load('assets/click.wav')

    def on_release(self):
        self.parent.typw.text += self.txt
        if abs(self.anim_y - self.default_y) >= .01:
            Animation(anim_y=self.default_y, d=.025, t='out_bounce').start(self)
        else:
            Animation(anim_y=self.anim_y + .005, d=.025, t='out_bounce').start(self)


class TextPaper(Image):
    """
    TypeWriter Paper
    """
    whiteout = ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Creating Blank Paper image to type on.
        # self.img = Im.open("paper.png")
        # self.img.resize((int(SCREEN_WIDTH *.75), SCREEN_HEIGHT))
        self.colour = 10, 10, 10, 255
        self.txt = Im.new('RGBA', (int(SCREEN_WIDTH * .75), PAPER_HEIGHT), (200, 200, 200, 255))
        self.default_pos = PAPER_WIDTH//2,  -(SCREEN_HEIGHT + PAPER_HEIGHT - STARTING_Y) // 8
        # Type writer does not type from the top rather type from the bottom.
        # self.txt = self.img.copy()
        self.head = {'x': STARTING_X, 'y': STARTING_Y}
        self.pos = self.default_pos
        self.size = [PAPER_WIDTH, PAPER_HEIGHT]
        self.first_letter = True
        self.font_size = None

    def update(self):
        """ Update the paper """
        data = BytesIO()
        i = self.letters[-1]
        # Type on the paper
        self.type(i)
        # Save updated txt (image) in data var to update the CoreImage Texture.
        self.txt.save(data, format='png')
        data.seek(0)
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.texture = im.texture

    def type(self, key):
        """ Type on the paper """
        # Render Text
        ImageDraw.Draw(self.txt).text((self.head["x"], self.head["y"]),
                                      key.char, font=key.font, fill=key.color)
        # Scrolling up
        # Shouldn't move paper if it is the first letter of the line
        if self.first_letter:
            self.first_letter = False
        else:
            self.pos[0] -= (self.char_size)

        self.font_size = key.font.getsize("l")[1]
        self.char_size = key.get_kerning()[0]
        self.head["x"] += self.char_size

        if (self.head["x"] - STARTING_X) + self.char_size >= PAPER_WIDTH:
            self.head["x"] = STARTING_X
            self.head["y"] += self.font_size
            self.y += self.font_size
            line_height = self.head["y"] - STARTING_Y
            self.pos = [self.default_pos[0], self.default_pos[1]+line_height]
            self.first_letter = True

    def escaped(self):
        if not self.font_size:
            return
        if self.text[-2:] == '_b':
            self.head["x"] -= self.char_size
            self.x += self.char_size
        elif self.text[-2:] == '_n':
            self.head['y'] += self.font_size
            self.head['x'] = STARTING_X
            self.y += self.font_size
            self.x = self.default_pos[0]

    def on_whiteout(self, *args):
        data = BytesIO()
        self.txt.paste(self.whiteout, (0,0), self.whiteout)
        self.txt.save(data, format='png')
        data.seek(0)
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.texture = im.texture

    def save(self):
        self.txt.save(f'{"".join(i.char for i in self.letters[:3])}.png')


class Pick(Popup):
    def __init__(self, typw, **kwargs):
        super().__init__(**kwargs)
        self.typw = typw


class WhiteOut(GestureSurface):
    def on_gesture_complete(self, gesture):
        fbo = Fbo(size=self.size,
            with_stencilbuffer=True)
        with fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()
            Scale(1, -1, 1)
            Scale(1, 1, 1)
            Translate(-self.x, -self.y - self.height, 0)
        fbo.add(self.canvas)
        fbo.draw()
        self.parent.typw.whiteout = Im.frombytes('RGBA', tuple(map(int, self.size)), fbo.texture.pixels)


class PhoneButtons(Label):
    ''' Phone Button/Label '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_event_type("on_button_touch_down")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch("on_button_touch_down", touch)
        return super().on_touch_down(touch)

    def on_button_touch_down(self, touch):
        ''' Actual Widget Press '''
        if self.collide_point(*self.pos):
            if touch.is_double_tap:
                self.parent.typw2.text = self.parent.typw2.text[:-1] + self.text[1]
            elif touch.is_triple_tap:
                self.parent.typw2.text = self.parent.typw2.text[:-1] + self.text[2]
            else:
                self.parent.typw2.text += self.text[0]
        return True


class JurassicJournalistApp(App):
    ''' App Class '''
    def build(self):
        Builder.load_file('buttons.kv')
        Builder.load_file('objects.kv')
        Window.size = SCREEN_WIDTH, SCREEN_HEIGHT
        return MainScreen()


if __name__ == '__main__':
    JurassicJournalistApp().run()
