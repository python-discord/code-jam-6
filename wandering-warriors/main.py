from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from modules import Abacus as AbacusBase
from modules import DrawPad
from modules.operations import OperationsLayout


class Calculator(Screen):
    pass


class Settings(Screen):
    pass


class TopMenu(Widget):
    pass


class Abacus(AbacusBase):
    pass


class OperationsBar(OperationsLayout):
    pass


class CuneiformDrawingInput(DrawPad):
    pass


class TopRightButton(Widget):
    pass


class ClearButton(Widget):
    pass


class HelpButton(Widget):
    pass


class SettingsButton(Widget):
    pass


class Screen:
    def __init__(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Calculator(name='calculator'))
        self.sm.add_widget(Settings(name='settings'))

    def get_manager(self):
        return self.sm


class CalculatorApp(App):
    TEXTURE = StringProperty('assets/graphics/wood.png')

    def build(self):
        return Screen().get_manager()


if __name__ == "__main__":
    CalculatorApp().run()
