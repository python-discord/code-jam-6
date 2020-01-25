from typing import List, Tuple, Union


class _Keycodes:
    """
    Returns multiple keycodes from
    a dictionary in one request.
    """
    def __init__(self) -> None:
        self.keys = {
            'enter':      13,
            'del':        127,
            'backspace':  8,
            'esc':        27,
            'c':          99,
            'x':          120,
            's':          115,
        }

    def __getitem__(self, items: Union[str, Tuple]) -> List[int]:
        if isinstance(items, str) or isinstance(items, int):
            items = [items]
        return [self.keys[item] for item in items]


KEYS = _Keycodes()

BASE_SIZE: int = 1024

UNITS: List[str] = [
    'B',
    'KB',
    'MB',
    'GB',
    'TB',
    'PB',
    'EB',
    'ZB',
    'YB'
]

MAX_PATH_LENGTH: int = 42
