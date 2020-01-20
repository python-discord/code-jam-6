from pathlib import Path
from threading import Thread
from datetime import datetime

from .constants import BASE_SIZE, UNITS


def bytes_conversion(size, unit=UNITS[0]):
    """
    Recursively converts bytes to the biggest
    possible unit without decimals.

    Returns the size and unit.
    """
    if size >= BASE_SIZE:
        return bytes_conversion(
            size//BASE_SIZE, 
            unit=UNITS[UNITS.index(unit)+1]
        )
    return str(size), unit

def threaded(func):
    """
    A decorator that runs a function on
    a separate thread.
    """
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        
    return wrapper

def file_info(ctx, dir_):
    name = type_ = size = date = ''

    if dir_ != '<-':
        path = Path(dir_)
        stats = path.stat()

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
    }
