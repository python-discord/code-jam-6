import random

from typing import List, Optional

from TLOA.core.constants import (
    Actions, AUDIO_PATH, TICK, NUMBER_OF_LANES, LANE_BOUNDS, SHIP_SPAWN_CHANCE,
    SHIP_SPAWN_RATE, GOLD_SHIP_CHANCE, LIGHT_SOURCE_POS, LIGHT_FOCUS_OFFSET,
    MIRROR_CANNON_RANGE
)
from TLOA.entities import MirrorCannon, BrownShip, GoldenShip, LightRays

from kivy import Logger
from kivy.clock import Clock, ClockEvent
from kivy.core.audio import Sound, SoundLoader
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, BoundedNumericProperty, NumericProperty
from kivy.vector import Vector


class Game(EventDispatcher):
    running = BooleanProperty(False)
    score = NumericProperty(0)
    health = BoundedNumericProperty(100, min=0, max=100,
                                    errorhandler=lambda x: 0 if x < 0 else 100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pause_game = False
        self.mirror = MirrorCannon()

        self._island_destroyed: Sound = SoundLoader.load(AUDIO_PATH.format("mirror_moving.wav"))
        self._mirror_moving: Sound = SoundLoader.load(AUDIO_PATH.format("mirror_moving.wav"))
        self._ship_destroyed: Sound = SoundLoader.load(AUDIO_PATH.format("ship_explosion.mp3"))

        # Create & initialize Mesh instance for Incident Sun rays
        self.sun_rays = LightRays(point=LIGHT_SOURCE_POS, surface=self.mirror.mirror_axis)

        # Create & initialize Mesh instance for Reflected Sun rays/Death Rays
        self.death_rays = LightRays(
            point=Vector(MIRROR_CANNON_RANGE, LANE_BOUNDS[self.mirror.state][1]),
            surface=self.mirror.mirror_axis)

        self.ship_lanes: List[List[BrownShip]] = [[] for _ in range(NUMBER_OF_LANES)]

        self._event: Optional[ClockEvent] = None
        self.register_event_type('on_add_ship')
        self.register_event_type('on_remove_ship')
        self.bind(health=self.on_health_change)

    def start(self):
        Logger.info('Start game')

        sound: Sound = SoundLoader.load(AUDIO_PATH.format("island_background.wav"))
        sound.loop = True
        sound.play()

        self.running = True

        Clock.schedule_interval(self.step, TICK)
        Clock.schedule_interval(lambda _: self.spawn_ship(), SHIP_SPAWN_RATE)

    def step(self, dt):
        if not self.running:
            return False

        elif self.pause_game == True:
            return
        # step ships and remove any dead ones
        for lane in self.ship_lanes:
            for ship in lane[:]:
                if ship.is_dead:
                    lane.remove(ship)
                    self.dispatch('on_remove_ship', ship)
                    Logger.info("%s died", ship)
                    continue

                ship.step(dt, self)

        # Trace Sun rays onto the mirror
        self.sun_rays.trace(point=LIGHT_SOURCE_POS, surface=self.mirror.mirror_axis)

        # Track the closest ship in the active lane
        if self.closest_ship:
            # focus the Death Rays to the ship's X position.
            death_rays_focus_x = self.closest_ship.shape.x + LIGHT_FOCUS_OFFSET.x

            # Deal damage to the ship.
            if self.closest_ship.id == GoldenShip.id:
                self.closest_ship.health -= 0.1    # Deal less Damage to Golden Ships

            if self.closest_ship.id == BrownShip.id:
                self.closest_ship.health -= 0.5    # Deal more Damage to Brown Ships.
        else:
            death_rays_focus_x = MIRROR_CANNON_RANGE

        # Trace Death rays onto the closest ship in the active lane.
        self.death_rays.trace(
            point=Vector(death_rays_focus_x,
                         LIGHT_FOCUS_OFFSET.y+LANE_BOUNDS[self.mirror.state][1]),
            surface=self.mirror.mirror_axis)

    # This property returns the closest ship in the active lane.
    @property
    def closest_ship(self):
        active_lane = self.mirror.state
        closest_ship = None
        for ship in self.ship_lanes[active_lane]:
            if ship.shape.x < MIRROR_CANNON_RANGE:
                if closest_ship:
                    if closest_ship.shape.x > ship.shape.x:
                        closest_ship = ship
                else:
                    closest_ship = ship
        return closest_ship

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

    def on_health_change(self, game, health):
        if health <= 0:
            self._island_destroyed.play()

    def on_add_ship(self, ship):
        pass

    def on_remove_ship(self, _ship):
        self._ship_destroyed.play()

    def process_action(self, action: Actions):
        if self.pause_game == True:
            return
        if action in (Actions.MOVE_LEFT, Actions.MOVE_UP):
            self._mirror_moving.play()
            self.mirror.state += 1
        elif action in (Actions.MOVE_RIGHT, Actions.MOVE_DOWN):
            self._mirror_moving.play()
            self.mirror.state -= 1
        return True
