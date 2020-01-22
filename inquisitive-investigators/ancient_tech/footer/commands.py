from typing import Any

from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
import pathlib


class BasePopup(Popup):

    def __init__(
            self, ctx: 'Footer', *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.ctx = ctx

    def on_dismiss(self, *args: Any, **kwargs: Any):
        self.ctx._open = False
        return super(BasePopup, self).on_dismiss(
            *args, **kwargs
        )


class AboutPopup(BasePopup):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ids.AboutInfo.text = '''
        Scroll Effect! Hopefully it works!
        
        Features:
                  yeah there here, we got like a file thing
                  Oh yeah and were adding a text editor too!
                  is this scrolling yet?
        '''


class Mkdir(BasePopup):
    left = NumericProperty()
    right = NumericProperty()

    def __init__(self, ctx: 'Footer', *args: Any, **kwargs: Any):
        super().__init__(ctx, *args, **kwargs)
        self.filemanager = 0

    def buttonselect(self, manager):
        self.left, self.right = 0, 0
        self.filemanager = manager
        if manager == 1:
            self.left = .2
        else:
            self.right = .2

    def mkdir(self, dir_name: str) -> None:
        if self.filemanager != 0 or dir_name != '':
            if self.filemanager == 1:
                dir_ = pathlib.Path(self.ctx.parent.ids.left.ids.header.ids.directory.text)
                new_dir = dir_ / dir_name

                new_dir.mkdir()

                self.ctx.parent.ids.left.ids.rv.dirs = dir_.iterdir()
                data = [self.ctx.parent.ids.left.ids.rv.generate(file_name) for file_name in self.ctx.parent.ids.left.ids.rv.dirs]

                if len(dir_.parts) > 1:
                    self.ctx.parent.ids.left.ids.rv.update(state=1, file=data)
                else:
                    self.ctx.parent.ids.left.ids.rv.update(state=2, file=data)

            elif self.filemanager == 2:
                dir_ = pathlib.Path(self.ctx.parent.ids.right.ids.header.ids.directory.text)
                new_dir = dir_ / dir_name

                new_dir.mkdir()

                self.ctx.parent.ids.right.ids.rv.dirs = dir_.iterdir()
                data = [self.ctx.parent.ids.right.ids.rv.generate(file_name) for file_name in self.ctx.parent.ids.right.ids.rv.dirs]

                if len(dir_.parts) > 1:
                    self.ctx.parent.ids.right.ids.rv.update(state=1, file=data)
                else:
                    self.ctx.parent.ids.right.ids.rv.update(state=2, file=data)
            self.dismiss()
        else:
            print('Please Enter a File Manager or Directory Name')


class QuitPopup(BasePopup):
    pass
