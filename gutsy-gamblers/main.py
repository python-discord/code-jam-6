import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
kivy.require('1.11.1')


class MainScreen(Screen):
    pass


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
