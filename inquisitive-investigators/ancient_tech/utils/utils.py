from threading import Thread

from .constants import UNITS

def bytes_conversion(size, unit=UNITS[0]):
    """
    Recursively converts bytes to the biggest
    possible unit without decimals.

    Returns the size and unit.
    """
    if size >= 1024:
        return bytes_conversion(
            size//1024, 
            unit=UNITS[UNITS.index(unit)+1]
        )
    return str(size), unit

def threaded(func):

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        
    return wrapper
