from pathlib import Path
from datetime import datetime

from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import (
    ObjectProperty,
    StringProperty
)


class NewFile(Button):
    ctx = ObjectProperty()
    txt = StringProperty()

    def on_release(self):
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

            self.parent.parent.parent.ids.header.current_dir = str(path)

        else:
            Logger.info('FileBrowser: Not a directory!')


class FileInfo(Label):
    pass
