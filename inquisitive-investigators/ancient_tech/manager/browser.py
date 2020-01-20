from pathlib import Path

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout

from .file import NewFile

Builder.load_file('./ancient_tech/manager/filemanager.kv')


class FileHeader(FloatLayout):
    current_dir = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_dir = str(Path().home())


class Files(StackLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.dirs = Path.home().iterdir()
        self.prev_dir = str(Path.home().parent)

    def generate(self, widget):
        self.add_widget(NewFile(self, str(widget), text=''))


class FileBrowser(FloatLayout):
    pass


class Column(Widget):
    pass


class Border(Widget):
    pass


class Header(Label):
    pass
