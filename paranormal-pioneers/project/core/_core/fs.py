import pathlib as pl
from typing import IO

from .apibase import ApiBase
from project.core._core.vm import OSApiException


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

    def exists_file(self, _path: str):
        path = self._to_full_path(_path)
        return path.exists()
