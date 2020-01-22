from enum import Enum, unique


ATLAS_PATH = "atlas://assets/{}"


@unique
class Actions(Enum):
    MOVE_LEFT = 'LEFT'
    MOVE_RIGHT = 'RIGHT'
    MOVE_UP = 'UP'
    MOVE_DOWN = 'DOWN'
    JUMP = 'JUMP'


KEY_MAPPING = {
    'w': Actions.MOVE_UP,
    'up': Actions.MOVE_UP,
    's': Actions.MOVE_DOWN,
    'down': Actions.MOVE_DOWN,
    'a': Actions.MOVE_LEFT,
    'left': Actions.MOVE_LEFT,
    'd': Actions.MOVE_RIGHT,
    'right': Actions.MOVE_RIGHT,
    'space': Actions.JUMP,
}
