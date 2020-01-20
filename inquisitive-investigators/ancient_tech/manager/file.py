from pathlib import Path
from datetime import datetime

from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.button import Button

from ..utils.utils import bytes_conversion


class NewFile(Button):

    def __init__(self, ctx, txt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.txt = txt
        self.ctx = ctx

        if self.txt != '<-':
            path = Path(txt)
            stats = path.stat()

            self.ids.name.text = path.name
            self.ids.date.text = datetime.fromtimestamp(
                stats.st_mtime
            ).strftime('%d-%m-%Y')

            if path.is_dir():
                t = 'DIR'

                self.ids.size.text = '-'
                # self.ids.size.text = ' '.join(
                #    bytes_conversion(
                #        sum(
                #            f.stat().st_size for f in path.glob('**/*') if f.is_file()
                #        )
                #    )
                # )

            else:

                if str(path).startswith('.') or path.suffix == '':
                    t = str(path.parts[-1])

                else:
                    t = path.suffix[1:].upper()
                
                self.ids.size.text = ' '.join(
                    bytes_conversion(
                        int(stats.st_size)
                    )
                )

            self.ids.type.text = t

        else:
            self.ids.name.text = '<-'
            self.ids.type.text = 'PARENT'

    def on_release(self):
        Logger.info(f'FileBrowser: Pressed "{self.txt}"')

        if self.txt == '<-':
            path = Path(self.ctx.prev_dir)
        else:
            path = Path(self.txt)

        if path.is_dir():
            self.ctx.clear_widgets()
            self.ctx.dirs = path.iterdir()

            if len(path.parts) > 1:
                self.ctx.prev_dir = str(path.parent)
                self.ctx.generate('<-')

            for d in self.ctx.dirs:
                self.ctx.generate(d)

            self.ctx.parent.parent.ids.header.current_dir = str(path)

        else:
            Logger.info('FileBrowser: Not a directory!')


class FileInfo(Label):
    pass
