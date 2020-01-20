from threading import Thread

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
