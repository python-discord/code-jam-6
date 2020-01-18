from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout


# Float Layout Documentation
# https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html
class Main(FloatLayout):
    pass


# Box Layout Documentation
# https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html?highlight=box%20layout
class FileMain(BoxLayout):
    pass


# Stack Layout Documentation
# https://kivy.org/doc/stable/api-kivy.uix.stacklayout.html?highlight=layout#kivy.uix.stacklayout.StackLayout.spacing
class FileBrowser(StackLayout):
    pass


# Label Will have to change to own Widget and take in fields such as Date, Time, File Size, etc...
# https://kivy.org/doc/stable/api-kivy.uix.label.html?highlight=label
class File(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Box Layout Documentation
# https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html?highlight=box%20layout
class Footer(BoxLayout):
    pass


# App Documentation
# https://kivy.org/doc/stable/api-kivy.app.html?highlight=app#module-kivy.app
class AncientTechApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    AncientTechApp().run()
