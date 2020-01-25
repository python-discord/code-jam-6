from functools import wraps
from typing import Any, Callable, IO, Generator, Iterable, List, Union

from project.core.constants import BIN_DIR, CANNOT_EXIT_ENV, FILE_SYSTEM
from project.core.path import Path

Function = Callable[[Any], Any]
PathLike = Union[str, Path]
FS = 'project.core.utils.FS'

ROOT = FILE_SYSTEM.resolve()
CURRENT = '.'
PARENT = '..'


def resolve_path() -> Function:
    def decorator(method: Function) -> Function:
        @wraps(method)
        def wrapper(fs: FS, path: str, *args, **kwargs) -> Any:
            def resolve(path: str) -> Path:
                return (ROOT / path).resolve()
            return method(fs, resolve(path), *args, **kwargs)
        return wrapper
    return decorator


class OSException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class FS:
    @resolve_path()
    def open_file(self, path: PathLike, mode: str) -> IO:
        if path.exists():
            return path.open(mode)
        raise OSException(f'error: file {path} does not exist')

    @resolve_path()
    def file_exists(self, path: PathLike) -> bool:
        return path.exists()

    @resolve_path()
    def iter_dir(self, path: PathLike) -> Generator[Path, None, None]:
        return path.iterdir()

    def resolve_commands(
        self, search_paths: Iterable[PathLike] = (BIN_DIR,)
    ) -> Generator[Path, None, None]:
        for path in search_paths:
            for file in filter(Path.is_file, self.iter_dir(path)):
                if file.suffix in {'.py'}:
                    yield file

    @resolve_path()
    def check_env(self, path: PathLike) -> bool:
        try:
            return bool(path.relative_to(ROOT))
        except ValueError:
            if CANNOT_EXIT_ENV:
                raise OSException('error: attempt to exit the environment')
            else:
                return False

    def get_path(
        self, before: PathLike, after: PathLike,
        check_existing: bool = True,
        check_dir: bool = True
    ) -> PathLike:
        new_path: PathLike = self.find_path(before, after)

        self.check_env(new_path)

        if not new_path.exists() and check_existing:
            raise OSException('error: path does not exist')

        if not new_path.is_dir() and check_dir and check_existing:
            raise OSException('error: not a directory')

        return new_path

    @resolve_path()
    def find_path(self, before: PathLike, after: PathLike) -> PathLike:
        path: Path = Path(before)
        parts: List[str] = Path(str(after)).parts

        for part in parts:
            if part == CURRENT:
                continue
            elif part == PARENT:
                path = path.parent
            else:
                path /= part

        self.check_env(path)

        return path

    @resolve_path()
    def is_file(self, path: PathLike) -> bool:
        return Path(path).is_file()
