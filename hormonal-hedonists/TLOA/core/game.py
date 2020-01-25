import random

from typing import List, Optional

from TLOA.entities.mirror_cannon import LIGHT_SOURCE_POS
from TLOA.core.constants import (
    Actions, TICK, NUMBER_OF_LANES, LANE_BOUNDS, SHIP_SPAWN_CHANCE,
    SHIP_SPAWN_RATE, GOLD_SHIP_CHANCE
)
from TLOA.entities import MirrorCannon, BrownShip, GoldenShip, LightRays

from kivy import Logger
from kivy.clock import Clock, ClockEvent
from kivy.event import EventDispatcher
from kivy.vector import Vector
from kivy.properties import BooleanProperty, BoundedNumericProperty, NumericProperty


class Game(EventDispatcher):
    running = BooleanProperty(False)
    score = NumericProperty(0)
    health = BoundedNumericProperty(100, min=0, max=100,
                                    errorhandler=lambda x: 0 if x < 0 else 100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mirror = MirrorCannon()

        # Create & initialize Mesh instance for Incident Sun rays
        self.sun_rays = LightRays(point=LIGHT_SOURCE_POS, surface=self.mirror.mirror_axis)

        # Create & initialize Mesh instance for Reflected Sun rays/Death Rays
        self.death_rays = LightRays(
            point=Vector(600, LANE_BOUNDS[self.mirror.state][1]),
            surface=self.mirror.mirror_axis)

        self.ship_lanes: List[List[BrownShip]] = [[] for _ in range(NUMBER_OF_LANES)]

        self._event: Optional[ClockEvent] = None
        self.register_event_type('on_add_ship')
        self.register_event_type('on_remove_ship')

    def start(self):
        Logger.info('Start game')
        self.running = True
        Clock.schedule_interval(self.step, TICK)
        Clock.schedule_interval(lambda _: self.spawn_ship(), SHIP_SPAWN_RATE)

    def step(self, dt):
        if not self.running:
            return False

        # Deal damage with mirror
        # Simulating damage
        if random.random() < 0.5:
            lane = self.ship_lanes[random.randrange(6)]
            if lane:
                lane[random.randrange(len(lane))].health -= 2

        # step ships and remove any dead ones
        for lane in self.ship_lanes:
            for ship in lane[:]:
                if ship.is_dead:
                    lane.remove(ship)
                    self.dispatch('on_remove_ship', ship)
                    Logger.info("%s died", ship)
                    continue

                ship.step(dt, self)

    def spawn_ship(self, override=False):
        if not self.running:
            return False

        if override or random.random() < SHIP_SPAWN_CHANCE:
            lane = random.randrange(NUMBER_OF_LANES)
            ship_class = random.choices([BrownShip, GoldenShip],
                                        weights=[1 - GOLD_SHIP_CHANCE, GOLD_SHIP_CHANCE])[0]
            ship = ship_class(lane)
            self.ship_lanes[lane].append(ship)
            self.dispatch('on_add_ship', ship)
            Logger.info("Ship Spawned at lane %d", lane)

    def on_add_ship(self, ship):
        pass

    def on_remove_ship(self, ship):
        pass

    def process_action(self, action: Actions):
        if action == Actions.MOVE_LEFT:
            print('Moving Left')
            self.mirror.state -= 1
        elif action == Actions.MOVE_RIGHT:
            print('Moving Right')
            self.mirror.state += 1
        elif action == Actions.MOVE_UP:
            self.mirror.state += 1
            print('Moving Up')
        elif action == Actions.MOVE_DOWN:
            self.mirror.state -= 1
            print('Moving Down')
        return True
