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
Hello thanks for using RexExplorer! made over the course of a week from CodeJam VI, RexExplorer is a TUI file explorer with a built in terminal with many features!
        
Features 
- Be able to experience what it was like to browse files and directories on your computer from the old days!
        
- A built in terminal? yeah we were suprised too! be able to change directories or even commit your own application to github!
        
- A built in editor too! What did you just want to look at your files, see what it was like to edit files back in the old'n days!
        
- Create files, New Directories to utilize your built in Editor, Terminal and File Explorer 
        '''


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
            if self.filemanager == 1:
                dir_ = Path(self.ctx.parent.ids.left.ids.header.ids.directory.current_dir)
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
                dir_ = Path(self.ctx.parent.ids.right.ids.header.ids.directory.current_dir)
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
        self.left = self.right = 0
        self.filemanager = manager
        if manager == 1:
            self.left = .2
        else:
            self.right = .2

    def mkfile(self, file_name: str) -> None:
        if self.filemanager != 0 or file_name != '':
            # Left Directory
            if self.filemanager == 1:
                dir_ = Path(self.ctx.parent.ids.left.ids.header.ids.directory.current_dir) / file_name
                if not dir_.exists():
                    dir_.touch()
                else:
                    print('File name already exists')
            # Right Directory
            elif self.filemanager == 2:
                dir_ = Path(self.ctx.parent.ids.right.ids.header.ids.directory.current_dir) / file_name
                if not dir_.exists():
                    dir_.touch()
                else:
                    print('File name already exists')
            else:
                print('Choose a browser side')
        else:
            Logger.info('MkDir: Enter a File name')

        path = Path(dir_)
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

        self.dismiss()


class QuitPopup(BasePopup):
    pass


def update(widget, directory):
    widget.ctx.parent.ids.left.ids.rv.dirs = directory.parent.iterdir()

    gen = widget.ctx.parent.ids.left.ids.rv.generate
    dirs = widget.ctx.parent.ids.left.ids.rv.dirs
    data = [gen(file_name) for file_name in dirs]

    if widget.ctx.parent.ids.left.ids.rv.selected is not None:

        if len(directory.parent.parts) > 1:
            state = 1
        else:
            state = 2

        widget.ctx.parent.ids.left.ids.rv.update(state=state, file=data)

    if widget.ctx.parent.ids.right.ids.rv.selected is not None:

        if len(directory.parent.parts) > 1:
            state = 1
        else:
            state = 2

        widget.ctx.parent.ids.right.ids.rv.update(state=state, file=data)
