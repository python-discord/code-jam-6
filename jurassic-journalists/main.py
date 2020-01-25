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
from kivy.uix import colorpicker
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty, NumericProperty # noqa
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from PIL import ImageDraw
from PIL import Image as Im


# Global Variables

# Screen Dimensions
# SCREEN_WIDTH = 540
# SCREEN_HEIGHT = 720
SCREEN_WIDTH, SCREEN_HEIGHT = Window.size
# Paper Dimensions
STARTING_X = 50 # PAPER_WIDTH - 240
STARTING_Y = 50 # PAPER_HEIGHT + 100
PAPER_WIDTH = SCREEN_WIDTH * .7 - STARTING_X
PAPER_HEIGHT = SCREEN_WIDTH

class MainScreen(ScreenManager):
    ''' ScreenManager '''


class RoomScreen(Screen):
    ''' Screen One '''


class PhoneScreen(Screen):
    ''' Screen Two '''


class TypeWriterButton(Button):
    sound = SoundLoader.load('click.wav')
    def on_release(self):
        self.parent.typw.text += self.txt
        if abs(self.anim_y - self.default_y) >= .01:
            Animation(anim_y = self.default_y, d=.025, t='out_bounce').start(self)
        else:
            Animation(anim_y = self.anim_y + .005, d=.025, t='out_bounce').start(self)
       


class TextPaper(Image):
    """
    TypeWriter Paper
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Creating Blank Paper image to type on.
        # self.img = Im.open("paper.png")
        # self.img.resize((int(SCREEN_WIDTH *.75), SCREEN_HEIGHT))
        self.colour = 255, 255, 255, 255
        self.txt = Im.new('RGBA', (int(SCREEN_WIDTH *.75), PAPER_HEIGHT), (200,200,200,255))
        self.default_pos = PAPER_WIDTH//2,  - abs((SCREEN_HEIGHT - PAPER_HEIGHT)//2) + STARTING_Y
        # Type writer does not type from the top rather type from the bottom.
        # self.txt = self.img.copy()
        self.head = {'x': STARTING_X, 'y': STARTING_Y}
        self.pos = self.default_pos
        self.size = [PAPER_WIDTH, PAPER_HEIGHT]

        self.first_letter = True
        self.font_size = None
        """
        self.mesh_texture = CoreImage('paper.png').texture
        Clock.schedule_interval(self.update_points, 0)
        """

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
        # Redner Text
        ImageDraw.Draw(self.txt).text((self.head["x"], self.head["y"]),
                                      key.char, font=key.font, fill=key.color)
        # Scrolling up

        # Shoudln't move paper if it is the first letter of the line
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
            #self.x = self.default_pos[0]

            # 10 is to adjust the height. If you guys can investigate why it is not
            # matching the height and width of letter defined in kv file that would be great.
            line_height = self.head["y"] - STARTING_Y - 10
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
        Window.borderless = False
        #pick = colorpicker.ColorPicker()
        #Window.add_widget(pick)
        #pick.bind(color = on_color)
        return MainScreen()

if __name__ == '__main__':
    JurassicJournalistApp().run()
