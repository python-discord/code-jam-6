import os
import sys
from pathlib import Path
from threading import Thread
from datetime import datetime
from typing import (
    Callable,
    Dict,
    Tuple,
    Union
)

from .constants import (
    BASE_SIZE, 
    UNITS, 
    MAX_PATH_LENGTH
)


def bytes_conversion(
        size: int, unit: str = UNITS[0]
) -> Tuple[str, str]:
    """
    Recursively converts bytes to the biggest
    possible unit without decimals.

    Returns the size and unit.
    """
    if size >= BASE_SIZE:
        return bytes_conversion(
            size // BASE_SIZE,
            unit=UNITS[UNITS.index(unit) + 1]
        )
    return str(size), unit


def threaded(func: Callable) -> Callable:
    """
    A decorator that runs a function on
    a separate thread.
    """

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    return wrapper


def file_info(
        ctx: 'RV', dir_: str
) -> Union[Dict[str, str], Dict[str, 'RV']]:
    """
    Returns information on the
    file/directory given.
    """
    name = type_ = size = date = ''

    if dir_ != '<-':
        path = Path(dir_)
        stats = path.stat()

        if len(path.name) > 22:
            name = path.name[:10] + '...'
        else:
            name = path.name

        date = datetime.fromtimestamp(
            stats.st_mtime
        ).strftime('%d-%m-%Y')

        if path.is_dir():
            t = 'DIR'

            size = '-'
            # size = ' '.join(
            #    bytes_conversion(
            #        sum(
            #            f.stat().st_size for f in path.glob('**/*') if f.is_file()
            #        )
            #    )
            # )

        else:

            if str(path).startswith('.') or path.suffix == '':
                t = str(path.parts[-1])

            else:
                t = path.suffix[1:].upper()

            size = ' '.join(
                bytes_conversion(
                    int(stats.st_size)
                )
            )

        type_ = t

    else:
        name = '<-'
        type_ = 'PARENT'

    return {
        'ctx': ctx,
        'txt': dir_,
        'name': name,
        'type': type_,
        'size_': size,
        'date': date,
        'alpha': 0
    }


def short_path(path: str) -> str:
    if len(path) > 50:
        parts = Path(path).parts

        for idx in range(len(parts)):
            p = str(Path(*parts[idx:]))

            if len(p) <= 50:
                return p

    return path
