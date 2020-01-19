'''Jurassic Journalists'''
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from PIL import ImageFont,ImageDraw
from PIL import Image as Im
from io import BytesIO
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
from math import sin, cos, pi
from kivy.core.window import Window


class JJ(App):
    ''' App Class '''
    def build(self):
        Window.borderless = True
        return Main()


class Main(ScreenManager):
    ''' ScreenManager '''


class TypeWriter(Screen):
    ''' Screen One '''


class Screen2(Screen):
    ''' Screen Two '''


class Pili(Image):
    """
    mesh_points = ListProperty([])
    mesh_texture = ObjectProperty(None)
    radius = NumericProperty(200)
    offset_x = NumericProperty(.5)
    offset_y = NumericProperty(.5)
    sin_wobble = NumericProperty(0)
    sin_wobble_speed = NumericProperty(0)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = Im.new("RGBA", (720,720), (200,200,200,0)) # Im.open('paper.png') #self.size
        self.txt = self.img.copy()
        self.head = {'x': 0, 'y': 0}
        self.draw = ImageDraw.Draw(self.txt)
        self.font_size = 0
        """
        self.mesh_texture = CoreImage('paper.png').texture
        Clock.schedule_interval(self.update_points, 0)
        """

    def update(self):
        data = BytesIO()
        i = self.letters[-1]
        self.draw.text((self.head["x"], self.head["y"]), i.char, font=i.font, fill=i.color)
        self.font_size =  i.font.getsize("l")[1]
        self.char_size = i.getKerning()[0]
        self.head["x"] += self.char_size
        if self.head["x"] +  self.char_size >= self.img.size[0]:
            self.head["x"] = 0 
            self.head["y"] += self.font_size
        
        self.txt.save(data, format='png')
        data.seek(0)
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.texture = im.texture

    def escaped(self):
        if not self.font_size:
            return
        if self.text[-2:] == '_b':
            self.head["x"] -= self.char_size
        elif self.text[-2:] == '_n':
            self.head['y'] += self.font_size
            self.head['x'] = 0
    """
    def update_points(self, *args):
        points = [Window.width / 2, Window.height / 2, .5, .5]
        i = 0
        while i < 2 * pi:
            i += 0.01 * pi
            points.extend([
                Window.width / 2 + cos(i) * (self.radius + self.sin_wobble * sin(i * self.sin_wobble_speed)),
                Window.height / 2 + sin(i) * (self.radius + self.sin_wobble * sin(i * self.sin_wobble_speed)),
                self.offset_x + sin(i),
                self.offset_y + cos(i)])

        self.mesh_points = points
    """

class Butt2(Label):
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


JJ().run()
