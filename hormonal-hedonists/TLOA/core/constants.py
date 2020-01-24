from enum import Enum, unique


TITLE = "The Legend of Archimedes"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

ATLAS_PATH = "atlas://assets/world/{}"
IMAGES_PATH = 'assets/images/{}'

TICK = 1 / 30  # 30 FPS

NUMBER_OF_LANES = 6
LANE_BOUNDS = [
    (300, 2), (300, 52), (300, 102), (300, 152), (300, 202), (300, 252)
]

SHIP_SPAWN_RATE = 1
SHIP_SPAWN_CHANCE = 1 / 5
MAX_SHIP_HEALTH = 100
GOLD_SHIP_CHANCE = 1 / 10


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
<<<<<<< HEAD

SHIP_IMAGE_MAPPING = {
    ShipType.BROWN: 'brown_ship',
    ShipType.GOLDEN: 'golden_ship'
}

SHIP_SCORE = {
    ShipType.BROWN: 1,
    ShipType.GOLDEN: 2
}

LANE_WIDTH = 50
LANE_NUMBER = 6
LANE_LENGTHS = [WINDOW_WIDTH, WINDOW_WIDTH, WINDOW_WIDTH, 1000, 900, 900]
=======
>>>>>>> master
