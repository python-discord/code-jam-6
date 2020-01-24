from typing import Any
from pathlib import Path
from shutil import rmtree

from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivy.logger import Logger


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
                dir_ = Path(self.ctx.parent.ids.left.ids.header.ids.directory.text)
                new_dir = dir_ / dir_name

                if not new_dir.exists():
                    new_dir.mkdir()
                else:
                    Logger.info('MkDir: Directory already exists')

                self.ctx.parent.ids.left.ids.rv.dirs = dir_.iterdir()
                data = [self.ctx.parent.ids.left.ids.rv.generate(file_name) for file_name in
                        self.ctx.parent.ids.left.ids.rv.dirs]

                if len(dir_.parts) > 1:
                    self.ctx.parent.ids.left.ids.rv.update(state=1, file=data)
                else:
                    self.ctx.parent.ids.left.ids.rv.update(state=2, file=data)

            elif self.filemanager == 2:
                dir_ = Path(self.ctx.parent.ids.right.ids.header.ids.directory.text)
                new_dir = dir_ / dir_name

                if not new_dir.exists():
                    new_dir.mkdir()
                else:
                    Logger.info('MkDir: Directory already exists')

                self.ctx.parent.ids.right.ids.rv.dirs = dir_.iterdir()
                data = [self.ctx.parent.ids.right.ids.rv.generate(file_name) for file_name in
                        self.ctx.parent.ids.right.ids.rv.dirs]

                if len(dir_.parts) > 1:
                    self.ctx.parent.ids.right.ids.rv.update(state=1, file=data)
                else:
                    self.ctx.parent.ids.right.ids.rv.update(state=2, file=data)
            self.dismiss()
        else:
            Logger.info('MkDir: Enter a directory name / Choose a browser side')


class DeletePopup(BasePopup):
    def __init__(self, ctx: 'Footer', *args: Any, **kwargs: Any):
        super().__init__(ctx, *args, **kwargs)
        self.filer = None
        self.filel = None
        self.getdirectory()

    def getdirectory(self):
        selectr = self.ctx.parent.ids.right.ids.rv.selected
        selectl = self.ctx.parent.ids.left.ids.rv.selected

        if selectr is not None:
            self.ids.right.text = f'Right Directory: {selectr.name}'
            self.filer = selectr
        else:
            self.ids.right.text = 'No File/Directory Selected'

        if selectl is not None:
            self.ids.left.text = f'Left Directory: {selectl.name}'
            self.filel = selectl
        else:
            self.ids.left.text = 'No File/Directory Selected'

    def delete(self):
        if self.filel is not None:
            self._remove(self.filel)

        if self.filer is not None:
            self._remove(self.filer)

        self.dismiss()

    def _remove(self, dir_) -> None:
        print(f'DIR NAME: {dir_.name} TEXT: {dir_.txt}')
        path = Path(dir_.txt)

        if dir_.type != 'DIR':
            path.unlink()
            Logger.info(f'Delete: Removed file {dir_.name}')
        else:
            rmtree(path)
            Logger.info(f'Delete: Removed directory {dir_.name}')

        self.ctx.parent.ids.left.ids.rv.dirs = path.parent.iterdir()

        gen = self.ctx.parent.ids.left.ids.rv.generate
        dirs = self.ctx.parent.ids.left.ids.rv.dirs
        data = [gen(file_name) for file_name in dirs]

        if self.ctx.parent.ids.left.ids.rv.selected is not None:

            if len(path.parent.parts) > 1:
                state = 1
            else:
                state = 2

            self.ctx.parent.ids.left.ids.rv.update(state=state, file=data)

        if self.ctx.parent.ids.right.ids.rv.selected is not None:

            if len(path.parent.parts) > 1:
                state = 1
            else:
                state = 2

            self.ctx.parent.ids.right.ids.rv.update(state=state, file=data)


class CreatePopup(BasePopup):
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


class QuitPopup(BasePopup):
    pass
