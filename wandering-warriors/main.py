from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder


class ToolManager(Widget):
    pass


class Abacus(Widget):
    pass


class DrawingInput(Widget):
    pass


class Ledger(Widget):
    pass


class AbacusApp(App):
    def build(self):
        Builder.load_file("abacus.kv")
        app = ToolManager()
        return app


if __name__ == "__main__":
    AbacusApp().run()
