from TLOA.core.constants import Actions
from TLOA.entities import MirrorCannon


class Game:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mirror = MirrorCannon()

    def start(self):
        pass

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
        return True
