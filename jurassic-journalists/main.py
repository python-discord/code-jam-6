'''Jurassic Journalists'''
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label


class JJ(App):
    ''' App Class '''
    def build(self):
        return Main()


class Main(ScreenManager):
    ''' ScreenManager '''


class TypeWriter(Screen):
    ''' Screen One '''


class Screen2(Screen):
    ''' Screen Two '''


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
