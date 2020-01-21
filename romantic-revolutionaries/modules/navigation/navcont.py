"""Navigation Controller Module"""
from enum import Enum


class Directions(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class NavControl:
    """Control navigation requests.

        To subscribe pass your callback function to subscribe()
        Your callback function should accept a direction and a distance.

        If an invalid direction is passed in a ValueError will be raised.

        go() is the public function called to effect navigation.
        If go() is called without arguments, it will repeat the last
        direction and distance. If it is called without a distance it will
        repeat the last distance. And if it is called without a direction
        it will repeat the last direction. If you want to call with a distance
        but no direction, you must do so with named argument for your distance.
    """

    def __init__(self):
        self.callbacks = set()
        self.last_distance = 1
        self.last_direction = Directions.NORTH

    def subscribe(self, callback):
        self.callbacks.add(callback)

    def unsubscribe(self, callback):
        self.callbacks.remove(callback)

    def _notify(self, direction, distance):
        for callback in self.callbacks:
            callback(direction, distance)

    def go(self, direction: Directions = None, distance: int = None):
        direction = self.last_direction if direction is None else direction
        distance = self.last_distance if distance is None else distance

        if not isinstance(direction, Directions):
            raise ValueError("Direction must a value of Directions")

        if distance == 0:
            raise ValueError("Distance can not be 0")

        self.last_direction = direction
        self.last_distance = distance

        self._notify(direction, distance)
