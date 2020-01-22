from TLOA.core.constants import Actions
from TLOA.entities.mirror import Mirror


class Game:
    def __init__(self):
        self.mirror = Mirror()

    def process_action(self, action: Actions):
        if action == Actions.MOVE_LEFT:
            print('Moving Left')
            self.mirror.state -= 1
        elif action == Actions.MOVE_RIGHT:
            print('Moving Right')
            self.mirror.state += 1
        elif action == Actions.MOVE_UP:
            print('Moving Up')
        elif action == Actions.MOVE_DOWN:
            print('Moving Down')
        elif action == Actions.JUMP:
            print('Jumping')
        return True
