from TLOA.core.constants import Actions
from TLOA.entities import MirrorCannon
from TLOA.entities import GoldenShip, BrownShip

from kivy import Logger
from kivy.clock import Clock


class Game:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mirror = MirrorCannon()
        self.ships = []
        self.total_spawned_ship = 0
        self.view = None

    def start(self, view):
        Logger.info('Start game')
        self.view = view
        Clock.schedule_interval(self.spawn_ship, 5)

    def spawn_ship(self, dt):
        self.total_spawned_ship += 1
        # TODO add code for ship position
        # TODO instead of create new ship, we can use existing one, so no need allocate new memory
        if self.total_spawned_ship % 10 == 0:
            # after 9 brown ships, we add new 1 golden ship
            Logger.info('Spawn new golden ship')
            new_ship = GoldenShip()
        else:
            Logger.info('Spawn new brown ship')
            new_ship = BrownShip()
        new_ship.bind(destroyed=self.on_ship_destroyed)
        self.ships.append(new_ship)
        self.view.show_ship(new_ship)

    def on_ship_destroyed(self, instance, new_state):
        if new_state:
            # ship is destroyed, remove it from view
            Logger.info('Remove ship')
            self.ships.remove(instance)
            # TODO update score

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
