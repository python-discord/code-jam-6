from pathlib import Path

from kivy.app import App
<<<<<<< HEAD
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
=======
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
>>>>>>> 387bc7cc5bd27fa85a4dad7296e28b9c28f1e883
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout


class Main(FloatLayout):
    pass


class FileMain(BoxLayout):
    def generate(self):
        dirs = Path.home().iterdir()

        for d in dirs:
            self.add_widget(File(text=str(d), size_hint=(1, .1)))


class FileBrowser(StackLayout):
    dirs = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dirs = Path.home().iterdir()
    

    def generate(self, widget):
        self.add_widget(File(text=str(widget)))


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
