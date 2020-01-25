from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from modules import Abacus as AbacusBase
from modules import DrawPad, LedgerLayout


class Calculator(Screen):
    pass


class Settings(Screen):
    pass


class TopMenu(Widget):
    pass


class Abacus(AbacusBase):
    pass


class Ledger(LedgerLayout):
    pass


class OperationsBar(Widget):
    def buttonImage(self, operation: str) -> str:
        return f'assets/graphics/{operation}.png'


class CuneiformDrawingInput(DrawPad):
    pass


class TopRightButton(Widget):
    pass


class Screen:
    def __init__(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Calculator(name='calculator'))

    def get_manager(self):
        return self.sm


class CalculatorApp(App):
    def build(self):
        return Screen().get_manager()


if __name__ == "__main__":
    CalculatorApp().run()
