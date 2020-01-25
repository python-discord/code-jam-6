from typing import Set


def get_all_subclasses(cls: type) -> Set[type]:
    """Return all subclasses of a give cls class."""
    return set(
        cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in get_all_subclasses(c)]
    )
