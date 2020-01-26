from kivy import Config

Config.set('kivy', 'window_icon', 'ancient_tech/static/icon.ico')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'minimum_width', '1300')
Config.set('graphics', 'minimum_height', '650')
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '650')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from .core import BrowserScreen
from ..footer.footer import Footer
from ..terminal.terminal import Terminal
from ..manager.browser import FileBrowser
from ..editor.editor import TextEditor
from ..photo_viewer.viewer import PhotoViewer
from ..utils.paths import CORE_KV

Builder.load_file(CORE_KV)


class Manager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.add_widget(BrowserScreen(name='browser'))
        self.add_widget(TextEditor(name='text_editor'))
        self.add_widget(PhotoViewer(name='photo_viewer'))


class AncientTechApp(App):

    def build(self):
        self.title = 'Rex Explorer'
        return Manager()
