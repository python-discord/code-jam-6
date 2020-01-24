from pathlib import Path

from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty)


class NewFile(Label):
    ctx = ObjectProperty()
    txt = StringProperty()
    alpha = NumericProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.ctx.select(file=self)
            if touch.is_double_tap:
                self.activate()

    def activate(self) -> None:
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

            current_path = ''
            for part in path.parts[-5:]:
                if len(part) > 10:
                    part = part[:5] + '..'
                if '\\' not in part:
                    current_path += part + '\\'
                else:
                    current_path += part

            self.parent.parent.parent.ids.header.current_dir = current_path[:-1]

        else:
            Logger.info('FileBrowser: Not a directory!')


class FileInfo(Label):
    pass
