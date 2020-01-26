from typing import Any, Union
from pathlib import Path
from shutil import (
    copy,
    copytree,
    rmtree,
    SameFileError
)

from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.properties import (
    NumericProperty,
    StringProperty
)

from ..utils.paths import ABOUT
from ..core.exceptions import (
    InvalidBrowser,
    InvalidSelection
)


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

    def update(self, browser_side: Union[str, int], dir_: str) -> None:
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


class DIRChoice(BasePopup):
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


class AboutPopup(BasePopup):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        with open(ABOUT, 'r') as f:
            self.ids.AboutInfo.text = f.read()


class CopyPopup(BasePopup):
    top_left = NumericProperty()
    top_right = NumericProperty()
    bottom_left = NumericProperty()
    bottom_right = NumericProperty()

    def __init__(self, ctx: 'Footer', *args: Any, **kwargs: Any) -> None:
        super().__init__(ctx, *args, **kwargs)
        self.to = None
        self.from_ = None

    def select(self, option: str, selection: str) -> None:
        """
        Store and validate selections.
        """
        if selection not in ('left', 'right'):
            raise InvalidSelection(
                'Selection must be either "left" or "right"'
            )

        if option == 'to':
            self.to = selection

            if selection == 'left':
                self.to = 'right'

                self.top_left = 0
                self.top_right = .2
                self.bottom_left = .2
                self.bottom_right = 0
            else:
                self.to = 'left'

                self.top_left = .2
                self.top_right = 0
                self.bottom_left = 0
                self.bottom_right = .2

        elif option == 'from':
            self.from_ = selection

            if selection == 'left':
                self.to = 'right'

                self.top_left = .2
                self.top_right = 0
                self.bottom_left = 0
                self.bottom_right = .2
            else:
                self.to = 'left'

                self.top_left = 0
                self.top_right = .2
                self.bottom_left = .2
                self.bottom_right = 0

        else:
            raise InvalidSelection(
                'Selection must be either "to" or "from"'
            )

    def copy(self) -> None:
        if self.from_ is None or self.to is None:
            Logger.info(
                'Copy: Please select a browser to copy to/from'
            )

        else:
            if self.from_ == 'left':
                from_ = self.ctx.parent.ids.left
                to = self.ctx.parent.ids.right
            else:
                from_ = self.ctx.parent.ids.right
                to = self.ctx.parent.ids.left

            try:
                from_obj = Path(from_.ids.rv.selected.txt)

            except AttributeError:
                Logger.info('Copy: Select a file/directory to copy')

            else:
                to_obj = Path(to.ids.header.ids.directory.current_dir)

                try:
                    if from_obj.is_dir():
                        copytree(from_obj, to_obj)
                    else:
                        copy(from_obj, to_obj)

                except SameFileError:
                    Logger.info('Copy: File already exists in this directory')

                except FileExistsError:
                    Logger.info('Copy: Directory already exists in this directory')

                else:
                    Logger.info(f'Copy: Copied {str(from_obj)} to {str(to_obj)}')

                    self.update('left', from_.ids.header.ids.directory.current_dir)
                    self.update('right', str(to_obj))

        self.dismiss()


class EditPopup(BasePopup):

    def __init__(self, ctx: 'Footer', *args: Any, **kwargs: Any) -> None:
        super().__init__(ctx, *args, **kwargs)

    def edit(self, side: str) -> None:
        if side == 'left':
            browser = self.ctx.parent.ids.left
        else:
            browser = self.ctx.parent.ids.right

        file = browser.ids.rv.selected
        manager = self.ctx.parent.parent.manager
        editor = manager.get_screen('text_editor')

        if file is not None and file.type != 'DIR':
            editor.editor.file_path = str(Path(file.txt))

            with open(Path(file.txt), 'r') as f:
                editor.editor.text = f.read()

            manager.current = 'text_editor'
        else:
            print('Editor: Please select a file')

        self.dismiss()


class Mkdir(DIRChoice):
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


class CreatePopup(DIRChoice):
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


class RenamePopup(DIRChoice):
    def rename(self, rename_text):
        if self.filemanager != 0 or rename_text != '':
            base = self.ctx.parent.ids

            if self.filemanager == 1:
                current = base.left.ids.header.ids.directory.current_dir
                select = self.ctx.parent.ids.left.ids.rv.selected
            elif self.filemanager == 2:
                current = base.right.ids.header.ids.directory.current_dir
                select = self.ctx.parent.ids.right.ids.rv.selected

            dir_check = Path(current) / rename_text

            if not dir_check.is_file():
                try:
                    Path(select.txt).rename(dir_check)

                except AttributeError:
                    Logger.info('Rename: Please select a file/directory')

                except FileExistsError:
                    Logger.info('Rename: Directory name already exists')

                else:
                    self.update(self.filemanager, current)
                    self.dismiss()

            else:
                Logger.info('Rename: File name already exists')

        else:
            Logger.info('Rename: Enter a File name')


class QuitPopup(BasePopup):
    pass
