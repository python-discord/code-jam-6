from pathlib import Path as BasePath
from shutil import copytree, copy2 as copy

PathType = type(BasePath())


class Path(PathType):
    def copy(self, destination: BasePath) -> None:
        if self.is_dir():
            func = copytree
            destination /= self.name
        else:
            func = copy

        src = str(self.resolve())
        dest = str(destination.resolve())

        func(src, dest)
