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
