import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
kivy.require('1.11.1')


class SettingsScreen(Popup):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        settings_popup = Popup(title="Settings", content=Label(text='Settings window!'),
                               size_hint=(None, None), size=(200, 200))
        settings_popup.open()


class MainScreen(Screen):
    def settings_button(self):
        SettingsScreen()


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('main.kv')
sm = WindowManager()

screens = [MainScreen(name='main')]
for screen in screens:
    sm.add_widget(screen)

sm.current = 'main'


class SunClock(App):
    """
    Core class.
    """
    def build(self):
        return sm


if __name__ == '__main__':
    SunClock().run()
