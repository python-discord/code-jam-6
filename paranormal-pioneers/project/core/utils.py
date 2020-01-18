from pathlib import Path
from typing import List, Union

from project.core.constants import CANNOT_EXIT_ENV, FILE_SYSTEM
from project.core.log import log

PathLike = Union[str, Path]

ROOT = FILE_SYSTEM.resolve()
CURRENT = '.'
PARENT = '..'


def check_env(path: PathLike):
    try:
        path.relative_to(ROOT)
        return True
    except ValueError:  # outside
        if CANNOT_EXIT_ENV:
            log.warning('error: attempt to exit the environment')
            return False


def change_dir(before: PathLike, after: PathLike) -> PathLike:
    new_dir: PathLike = find_dir(before, after)

    if not check_env(new_dir):
        return before

    if not new_dir.exists():
        log.warning('error: path does not exist')
        return before

    if new_dir.is_file():
        log.warning('error: cannot accept files')
        return before

    return new_dir


def find_dir(before: PathLike, after: PathLike) -> PathLike:
    path: Path = Path(before)
    parts: List[str] = Path(str(after)).parts

    for part in parts:
        if part == CURRENT:
            continue
        elif part == PARENT:
            path = path.parent
        else:
            path /= part

    return path
