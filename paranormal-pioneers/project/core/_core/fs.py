import pathlib as pl
from typing import IO, List, Generator, Union

from project.core.log import log
from .apibase import ApiBase
from project.core._core.vm import OSApiException
PathLike = Union[str, pl.Path]


# TODO: use a decorator instead of _to_full_path
class FsApi(ApiBase):
    def _to_full_path(self, path: str) -> pl.Path:
        return self.env.fs_root / path

    def open_file(self, _path: str, mode: str) -> IO:
        path = self._to_full_path(_path)
        if path.exists():
            return path.open(mode)
        else:
            raise OSApiException(f"File '{path}' does not exist")

    def exists_file(self, _path: str)->bool:
        path = self._to_full_path(_path)
        return path.exists()

    def list_dir(self, _path: str)->Generator[pl.Path, None, None]:
        path = self._to_full_path(_path)
        yield from path.iterdir()

    def resolve_commands(self, search=('./bin',)) -> Generator[pl.Path, None, None]:
        for _path in search:
            for file in filter(pl.Path.is_file, self.list_dir(_path)):
                if file.suffix == '.py':
                    yield file

    def check_env(self, path: str):
        fpath = self._to_full_path(path)
        try:
            fpath.relative_to(self.env.fs_root)
            return True
        except ValueError:  # outside
            if self.env.ex_env:
                log.warning('error: attempt to exit the environment')
                return False

    def change_dir(self, before: str, after: PathLike) -> PathLike:
        new_dir: PathLike = self.find_dir(before, after)

        if not self.check_env(new_dir):
            return before
        fpath = self._to_full_path(new_dir)
        if not fpath.exists():
            log.warning('error: path does not exist')
            return before

        if fpath.is_file():
            log.warning('error: cannot accept files')
            return before

        return fpath.relative_to(self.env.fs_root)

    def find_dir(self, before: str, after: PathLike) -> PathLike:
        path: pl.Path = self._to_full_path(before)
        # parts: Tuple[str, ...] = .parts
        path /= pl.Path(str(after))
        return path.relative_to(self.env.fs_root)

    def is_file(self, _path: str):
        return self._to_full_path(_path).is_file()

    def touch(self, _path: str):
        return self._to_full_path(_path).touch()