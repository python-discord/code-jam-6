"""Map Controller Module."""
from modules.navigation.navcont import Directions


class DungeonMap:
    """Control the dungeon map."""

    map_vector = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 9, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    #             [[0, 0, 0, 0],
    #              [0, 1, 1, 0],
    #              [0, 1, 1, 0],
    #              [0, 0, 0, 0]]

    def __init__(self):
        """Initialize instance."""
        self.callbacks = set()
        self.current_location = (1, 1)
        self.visible_block = []
    #                       [[0, 0, 0],
    #                        [0, 1, 1],
    #                        [0, 1, 1]]
        self.did_bonk = False

    def subscribe(self, callback):
        """Subscribe to this classes messages."""
        self.callbacks.add(callback)

    def unsubscribe(self, callback):
        """Unsubscribe from this classes messages."""
        self.callbacks.remove(callback)

    def callback(self, direction, distance):
        """Use this function to subscribe to other classes messages."""
        self.did_bonk = False
        row, col = 0, 0
        if direction == Directions.NORTH:
            row = -1
        elif direction == Directions.SOUTH:
            row = 1
        elif direction == Directions.EAST:
            col = 1
        elif direction == Directions.WEST:
            col = -1

        new_location = self.current_location
        for d in range(distance):
            new_location = new_location[0] + row, new_location[1] + col
            if DungeonMap.map_vector[new_location[0]][new_location[1]] == 0:
                self.did_bonk = True
                new_location = new_location[0] - row, new_location[1] - col
                break

        self.current_location = new_location

        self._notify()

    def _notify(self):
        """Send all the messages to the subscribers."""
        for sub in self.callbacks:
            sub(self.current_location, self.visible_block, self.did_bonk)
