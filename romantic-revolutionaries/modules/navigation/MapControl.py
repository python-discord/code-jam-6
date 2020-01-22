"""Map Controller Module."""
from navcont import Directions


class DungeonMap():
  map_vector = [[0,0,0,0],
                [0,1,1,0],
                [0,1,1,0],
                [0,0,0,0]]

  def __init__(self):
    self.subscribers = set()
    self.current_location = (1, 1)
    self.visible_block = [[0,0,0],
                          [0,1,1],
                          [0,1,1]]
    self.did_bonk = False

  def subscribe(self, callback):
    self.callbacks.add(callback)

  def unsubscribe(self, callback):
    self.callbacks.remove(callback)

  def callback(self, direction, distance):
    # handle movement to new current_location
    # update did_bonk
    # update visible_block update
    x, y = 0, 0
    if direction == Directions.NORTH:
        y = -1
    elif direction == Directions.SOUTH:
        y = 1
    elif direction == Directions.EAST:
        x = 1
    elif direction == Directions.WEST:
        x = -1

    new_loc = current_location
    for d in distance:
        new_loc = new_loc + (x, y)
        if map_vector[new_loc[0]][new_loc[1]] == 0:
            self.did_bonk = True
            new_loc = new_loc - (x, y)
            break;

    self.current_location = new_location

    notify(self)

  def notify(self):
    for sub in self.subscribers:
      sub(self.current_location, self.visible_block, self.did_bonk)

