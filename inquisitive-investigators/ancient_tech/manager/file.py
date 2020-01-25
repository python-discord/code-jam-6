from pathlib import Path

from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty
)

from ..utils.utils import short_path


class NewFile(Label):
    ctx = ObjectProperty()
    txt = StringProperty()
    alpha = NumericProperty()
    browser = ObjectProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.ctx.select(file=self)

            if touch.is_double_tap:
                self.activate()

    def activate(self) -> None:
        """
        Opens the file/directory that was selected.
        """
        Logger.info(f'FileBrowser: Pressed "{self.txt}"')

        if self.txt == '<-':
            path = Path(self.ctx.prev_dir)
        else:
            path = Path(self.txt)

        if path.is_dir():
            self.ctx.data = [self.ctx.generate('<-')]
            self.ctx.dirs = path.iterdir()

            data = [self.ctx.generate(file_name) for file_name in self.ctx.dirs]

            if len(path.parts) > 1:
                self.ctx.prev_dir = str(path.parent)
                self.ctx.update(state=1, file=data)
            else:
                self.ctx.update(state=2, file=data)

            self.parent.parent.parent.ids.header.dir_name = short_path(str(path))
            self.parent.parent.parent.ids.header.current_dir = str(path)

        else:
            Logger.info('FileBrowser: Not a directory!')


class FileInfo(Label):
    pass
