from kivy import Config

Config.set('kivy', 'window_icon', 'ancient_tech/static/icon.png')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', '0')
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

from .core import BrowserScreen
from ..footer.footer import Footer
from ..terminal.terminal import Terminal
from ..manager.browser import FileBrowser
from ..editor.editor import TextEditor

Builder.load_file('./ancient_tech/core/core.kv')


class Manager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.add_widget(BrowserScreen(name='browser'))
        self.add_widget(TextEditor(name='text_editor'))


class AncientTechApp(App):

    def build(self):
        self.title = 'Rex Explorer'
        return Manager()
