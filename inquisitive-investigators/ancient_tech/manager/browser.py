from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Union

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import _cached_views, _view_base_cache
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import (
    ObjectProperty,
    StringProperty
)

from .file import NewFile
from ..utils.utils import file_info, short_path

Builder.load_file('./ancient_tech/manager/filemanager.kv')


class FileHeader(FloatLayout):
    """
    Displays the current directory
    in the header.
    """
    current_dir = StringProperty()
    dir_name = StringProperty()
    directory = ObjectProperty()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.current_dir = str(Path.home())
        self.dir_name = short_path(str(Path.home()))


class RV(RecycleView):
    """
    This is one side of the file browser.

    One instance is used for each side.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.dirs = Path.home().iterdir()
        self.prev_dir = str(Path.home().parent)

        self.update(state=0, file=[])
        self.selected = None
        self.prev_selected = None

    def generate(self, f: Any) -> Union[
        Dict[str, str], Dict[str, RV]
    ]:
        return file_info(self, str(f))

    def update(self, state: int, file: List[str]) -> None:
        """
        Refreshes the browser with the newly
        updated files/directories.
        """
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
        """
        Highlights the file/directory that is selected.

        Only allows one object to be selected at a time.
        """
        if self.prev_selected is not None and self.selected.name == file.name:

            self.selected.alpha = 0
            self.prev_selected.alpha = 0
            for fileDict in self.data:
                if fileDict['alpha'] == .5:
                    fileDict['alpha'] = 0

            self.prev_selected = None
            self.selected = None
            return None

        if file.type != 'PARENT':
            if self.prev_selected is not None:

                # Reset all Alpha values in self.data
                self.selected.alpha = 0
                self.prev_selected.alpha = 0
                for fileDict in self.data:
                    if fileDict['alpha'] == .5:
                        fileDict['alpha'] = 0

            self.prev_selected = file
            self.selected = file

            # Set selected to Alpha value
            self.prev_selected.alpha = .5
            self.selected.alpha = .5
            for fileDict in self.data:
                if fileDict['name'] in [self.selected.name, self.prev_selected.name]:
                    fileDict['alpha'] = .5


class FileBrowser(FloatLayout):
    recycle_view = ObjectProperty()
    header = ObjectProperty()


class Files(RecycleBoxLayout):
    pass


class Column(Widget):
    pass


class Border(Widget):
    pass


class Header(Label):
    pass
