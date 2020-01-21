from kivy import Config

Config.set('graphics', 'minimum_width', '1300')
Config.set('graphics', 'minimum_height', '650')
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '650')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import (
    ScreenManager,
    Screen
)

from .footer.footer import Footer
from .terminal.terminal import Terminal
from .manager.browser import FileBrowser
from .editor.editor import TextEditor

Builder.load_file('./ancient_tech/main.kv')


class Main(Screen, FloatLayout):
    pass


class Manager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.add_widget(TextEditor(name='text_editor'))
        self.add_widget(Main(name='browser'))


class AncientTechApp(App):

    def build(self):
        return Main()


if __name__ == '__main__':
    AncientTechApp().run()
