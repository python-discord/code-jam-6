from enum import Enum, unique
from kivy.vector import Vector


TITLE = "The Legend of Archimedes"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

ATLAS_PATH = "atlas://assets/world/{}"
IMAGES_PATH = 'assets/images/{}'
AUDIO_PATH = 'assets/sfx/{}'

TICK = 1 / 30  # 30 FPS

NUMBER_OF_LANES = 6
LANE_BOUNDS = [
    (300, 2), (300, 52), (300, 102), (300, 152), (300, 202), (300, 252)
]

SHIP_SPAWN_RATE = 1
SHIP_SPAWN_CHANCE = 1 / 5
MAX_SHIP_HEALTH = 100
GOLD_SHIP_CHANCE = 1 / 10

MIRROR_DIAMETER = 80
MIRROR_CANNON_POS = Vector(150, 260)
MIRROR_CANNON_RANGE = 900
MIRROR_OFFSET = Vector(97, 78)
MIRROR_ANGLES = [
    75, 90, 105, 120, 135, 150
]

LIGHT_SOURCE_POS = Vector(700, 620)
LIGHT_FOCUS_POS = Vector(600, 50)
LIGHT_FOCUS_OFFSET = Vector(100, 100)
LIGHT_COLOR_MAX_HUE = 0.5
LIGHT_COLOR_MAX_SATURATION = 0.8
LIGHT_COLOR_MAX_VALUE = 1.0
LIGHT_COLOR_MAX_ALPHA = 0.65


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
