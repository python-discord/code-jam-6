from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Union

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout

from .file import NewFile
from ..utils.utils import file_info

Builder.load_file('./ancient_tech/manager/filemanager.kv')


class FileHeader(FloatLayout):
    current_dir = StringProperty()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.current_dir = str(Path().home())


class RV(RecycleView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.dirs = Path.home().iterdir()
        self.prev_dir = str(Path.home().parent)

        self.update(state=0, file=[])
        self.selected = None
        self.prev_selected  = None

    def generate(
            self, f: Any
    ) -> Union[Dict[str, str], Dict[str, RV]]:
        return file_info(self, str(f))

    def update(self, state: int, file: List[str]) -> None:
        if state == 0:
            self.data = [
                self.generate('<-'),
                *(self.generate(file_name) for file_name in self.dirs)
            ]
        elif state == 1:
            self.data = [self.generate('<-'), *file]
        elif state == 2:
            self.data = file

    def select(self, file):
        # When nothing is selected
        if self.prev_selected is not None:
            self.prev_selected.alpha = 0

        self.prev_selected = file
        self.selected = file
        file.alpha = .5


class Files(RecycleBoxLayout):
    pass


class FileBrowser(FloatLayout):
    pass


class Column(Widget):
    pass


class Border(Widget):
    pass


class Header(Label):
    pass
