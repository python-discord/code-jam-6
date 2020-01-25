from typing import Any
from pathlib import Path
from shutil import rmtree

from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivy.logger import Logger

from ..core.exceptions import InvalidBrowser

class BasePopup(Popup):

    def __init__(
            self, ctx: 'Footer', *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.opp_update = False

    def on_dismiss(self, *args: Any, **kwargs: Any) -> None:
        self.ctx._open = False
        return super(BasePopup, self).on_dismiss(
            *args, **kwargs
        )

    def update(self, browser_side: str, dir_: str) -> None:
        """
        Refreshes the specified browser side.
        """
        dir_ = Path(dir_)
        base = self.ctx.parent.ids

        if browser_side in ('left', 1):
            browser = base.left.ids.rv
            browser_side = 'left'

        elif browser_side in ('right', 2):
            browser = base.right.ids.rv
            browser_side = 'right'

        else:
            raise InvalidBrowser(
                'Browser side should be either "left" or "right"'
            )

        browser.dirs = dir_.iterdir()

        gen = browser.generate
        dirs = browser.dirs
        data = [gen(file_name) for file_name in dirs]

        # Determine whether a back button should
        # be generated. Based on whether the current
        # directory is the root directory or not.
        if len(dir_.parts) > 1:
            browser.update(state=1, file=data)
        else:
            browser.update(state=2, file=data)

        # If the opposite side is the same directory,
        # update it too
        if not self.opp_update:

            if browser_side == 'left':
                opp_dir = base.right.ids.header.ids.directory.current_dir

                if opp_dir == str(dir_):
                    self.opp_update = True
                    self.update('right', opp_dir)

            else:
                opp_dir = base.left.ids.header.ids.directory.current_dir

                if opp_dir == str(dir_):
                    self.opp_update = True
                    self.update('left', opp_dir)

        else:
            self.opp_update = False
            

class AboutPopup(BasePopup):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        with open('ancient_tech/static/about.txt', 'r') as f:
            self.ids.AboutInfo.text = f.read()
            

class EditPopup(BasePopup):

    def __init__(self, ctx: 'Footer', *args: Any, **kwargs: Any) -> None:
        super().__init__(ctx, *args, **kwargs)
        self.ctx = ctx

    def edit(self, side: str) -> None:
        if side == 'left':
            browser = self.ctx.parent.ids.left
        else:
            browser = self.ctx.parent.ids.right

        file = browser.ids.rv.selected
        manager = self.ctx.parent.parent.manager
        editor = manager.get_screen('text_editor')

        if file is not None:
            editor.editor.file_path = str(Path(file.txt))

            with open(Path(file.txt), 'r') as f:
                editor.editor.text = f.read()

            manager.current = 'text_editor'
            self.dismiss()


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
            dir_ = self.ctx.parent.ids

            if self.filemanager == 1:
                dir_ = Path(dir_.left.ids.header.ids.directory.current_dir)
                new_dir = dir_ / dir_name

            elif self.filemanager == 2:
                dir_ = Path(dir_.right.ids.header.ids.directory.current_dir)
                new_dir = dir_ / dir_name


            if not new_dir.exists():
                new_dir.mkdir()

                self.update(self.filemanager, dir_)
                self.dismiss()
            else:
                Logger.info('MkDir: Directory already exists')

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
        path = Path(dir_.txt)

        if dir_.type != 'DIR':
            path.unlink()
            Logger.info(f'Delete: Removed file {dir_.name}')
        else:
            rmtree(path)
            Logger.info(f'Delete: Removed directory {dir_.name}')

        dir_ = path.parent

        if self.ctx.parent.ids.left.ids.rv.selected is not None:
            self.update('left', dir_)

        if self.ctx.parent.ids.right.ids.rv.selected is not None:
            self.update('right', dir_)


class CreatePopup(BasePopup):
    left = NumericProperty()
    right = NumericProperty()

    def __init__(self, ctx: 'Footer', *args: Any, **kwargs: Any):
        super().__init__(ctx, *args, **kwargs)
        self.filemanager = 0

    def buttonselect(self, manager):
        self.left = self.right = 0
        self.filemanager = manager
        if manager == 1:
            self.left = .2
        else:
            self.right = .2

    def mkfile(self, file_name: str) -> None:
        if self.filemanager != 0 or file_name != '':
            base = self.ctx.parent.ids

            if self.filemanager == 1:
                current = base.left.ids.header.ids.directory.current_dir

            elif self.filemanager == 2:
                current = base.right.ids.header.ids.directory.current_dir
                
            dir_ = Path(current) / file_name
                
            if not dir_.exists():
                dir_.touch()
        
                self.update(self.filemanager, current)
                self.dismiss()

            else:
                Logger.info('Create: File already exists')
            
        else:
            Logger.info('Create: Enter a File name')


class QuitPopup(BasePopup):
    pass
