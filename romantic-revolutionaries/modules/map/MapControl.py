"""Map Controller Module."""
from modules.map.RoomControl import EmptyCavePath
from modules.navigation.navcont import Directions


class DungeonMap:
    """Control the dungeon map."""

    map_vector = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self):
        """Initialize instance."""
        self.callbacks = set()
        self.current_location = (1, 1)
        self.visible_block = self._get_visible_block()
        #                       [[0, 0, 0],
        #                        [0, 1, 1],
        #                        [0, 1, 1]]
        self.did_bonk = False
        self.rooms = self.load_map()

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
        self.visible_block = self._get_visible_block()

        self._notify()

    def _notify(self):
        """Send all the messages to the subscribers."""
        for sub in self.callbacks:
            # try:
            #     room = self.rooms[self.current_location]
            # except:
            #     room = None
            # sub(self.current_location, room, self.visible_block, self.did_bonk)
            sub(self.current_location, self.visible_block, self.did_bonk)

    def _get_visible_block(self):
        visible_block = [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]

        for y in range(-1, 2):
            for x in range(-1, 2):
                visible_block[y + 1][x + 1] = DungeonMap.map_vector[self.current_location[0] + y][
                    self.current_location[1] + x]

        return visible_block

    def load_map(self):
        room_map = {}
        for y in range(len(DungeonMap.map_vector)):
            for x in range(len(DungeonMap.map_vector)):
                if DungeonMap.map_vector[y][x] == 1:
                    room_map[(y, x)] = EmptyCavePath()
        return room_map
