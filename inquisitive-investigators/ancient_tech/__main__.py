from kivy import Config

Config.set('graphics', 'minimum_width', '1300')
Config.set('graphics', 'minimum_height', '650')
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '650')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from .footer.footer import Footer
from .terminal.terminal import Terminal
from .manager.browser import FileBrowser

Builder.load_file('./ancient_tech/main.kv')


class Main(FloatLayout):
    pass


class AncientTechApp(App):

    def build(self):
        return Main()


if __name__ == '__main__':
    AncientTechApp().run()
