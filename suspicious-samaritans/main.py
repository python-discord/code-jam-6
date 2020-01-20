import atexit
import os

from kivy.app import App
from kivy.config import Config
from kivy.lang.builder import Builder

from frontend.gui.root import TabbedRoot

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')

Builder.load_file("frontend/gui/custom_widgets.kv")
Builder.load_file("frontend/gui/videocontainer.kv")
Builder.load_file("frontend/gui/root.kv")


class VCRApp(App):
    """App class for the ager video editor"""
    use_kivy_settings = False

    def build(self):
        return TabbedRoot()


def cleanup():
    os.remove(".thumbnail.png")


if __name__ == "__main__":
    atexit.register(cleanup)
    VCRApp().run()
