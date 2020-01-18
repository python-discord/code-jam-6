from pathlib import Path

from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout


class Main(FloatLayout):
    pass


class FileBrowser(StackLayout):
    dirs = ObjectProperty(None)
    size_hint = (1, None)

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.dirs = Path.home().iterdir()

    def generate(self, widget):
        self.add_widget(File(text=str(widget)))


class SubBrowser(StackLayout):
    dirs = ObjectProperty(None)
    size_hint = (1, None)

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.dirs = Path.home().iterdir()

    def generate(self, widget):
        self.add_widget(File(text=str(widget)))


class File(Button):
    pass


class Footer(BoxLayout):
    pass


class AncientTechApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    AncientTechApp().run()
