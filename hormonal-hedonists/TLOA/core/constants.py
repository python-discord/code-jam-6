from enum import Enum, unique

from TLOA.entities import ShipType


TITLE = "The Legend of Archimedes"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

ATLAS_PATH = "atlas://assets/world/{}"
IMAGES_PATH = 'assets/images/{}'


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

SHIP_IMAGE_MAPPING = {
    ShipType.BROWN: 'brown_ship',
    ShipType.GOLDEN: 'golden_ship'
}

SHIP_SCORE = {
    ShipType.BROWN: 1,
    ShipType.GOLDEN: 2
}

LANE_NUMBER = 6
LANE_LENGTHS = [WINDOW_WIDTH, WINDOW_WIDTH, WINDOW_WIDTH, 1000, 900, 900]
