"""Control the view."""
from modules.navigation.navcont import Directions


class ViewControl():
    def __init__(self):
        self.callbacks = set()
        self.view_description = ''
        self.current_location = None
        self.visible_block = None
        self.did_bonk = False

    def subscribe(self, callback):
        """Subscribe to this classes messages."""
        self.callbacks.add(callback)

    def unsubscribe(self, callback):
        """Unsubscribe from this classes messages."""
        self.callbacks.remove(callback)

    def callback(self, current_location, visible_block, did_bonk):
        """Use this function to subscribe to other classes messages."""
        self.current_location = current_location
        self.visible_block = visible_block
        self.did_bonk = did_bonk
        print(self.current_location)
        print(self.did_bonk)
        for v in visible_block:
            print(v)

        self._notify()

    def _notify(self):
        """Send all the messages to the subscribers."""
        for sub in self.callbacks:
            sub(self.view_description)

    def look(self, direction):
        self.view_description = ''

        down_view = self.visible_block[1][1]

        if direction == Directions.NORTH:
            forward_view = self.visible_block[0]
        elif direction == Directions.SOUTH:
            forward_view = self.visible_block[2]
        elif direction == Directions.EAST:
            forward_view = list(zip(*list(reversed(self.visible_block))))[0]
            pass
        elif direction == Directions.WEST:
            forward_view = list(reversed(list(zip(*list(self.visible_block)))))[0]

        if self.did_bonk:
            self.view_description += 'You have run into a wall.\n'

        if forward_view[1] == 0:
            self.view_description = 'There is a wall in front of you.\n'
        else:
            self.view_description = 'There is a dark passage ahead of you.\n'

        self.view_description += 'It is bordered to the left with '
        if forward_view[0] == 0:
            self.view_description += 'a wall.\n'
        elif forward_view[0] == 1:
            self.view_description += 'a dark passage.\n'
        else:
            self.view_description += f'a {forward_view[0]}.\n'

        self.view_description += 'It is bordered to the right with '
        if forward_view[2] == 0:
            self.view_description += 'a wall.\n'
        elif forward_view[2] == 1:
            self.view_description += 'a dark passage.\n'
        else:
            self.view_description += f'a {forward_view[0]}.\n'

        if down_view != 1:
            self.view_description += f'At your feet there is {down_view}.\n'

        self._notify()
