from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout


class Main(FloatLayout):
    pass


class FileMain(BoxLayout):
    def generate(self):
        dirs = Path.home().iterdir()

        for d in dirs:
            self.add_widget(File(text=str(d), size_hint=(1, .1)))


class FileBrowser(StackLayout):
    pass


class SubBrowser(StackLayout):
    pass


class File(Button):
    pass


class Footer(BoxLayout):
    pass


class AncientTechApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    AncientTechApp().run()
