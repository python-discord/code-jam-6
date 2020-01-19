from kivy.config import Config
from kivy.lang.builder import Builder
from kivy.app import App

from frontend.gui.root import RootLayout

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')

Builder.load_file("frontend/gui/root.kv")


class VCRApp(App):
    """App class for the ager video editor"""

    def build(self):
        return RootLayout()


if __name__ == "__main__":
    VCRApp().run()
