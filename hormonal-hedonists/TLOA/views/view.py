import math

from random import randint

from TLOA.core.game import Game
from TLOA.core.constants import (ATLAS_PATH, IMAGES_PATH, KEY_MAPPING, WINDOW_WIDTH,
                                 WINDOW_HEIGHT, LANE_BOUNDS)
from TLOA.entities.mirror_cannon import LIGHT_SOURCE_POS
from TLOA.views import ShipView

from kivy import Logger
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.vector import Vector


class GameView(Widget):
    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)
        self._game = game

        game.mirror.bind(state=self.on_mirror_state_change)
        game.bind(running=lambda _, value: self.show_game(value))
        game.bind(score=self.on_score_change)
        game.bind(health=self.on_island_health_change)
        game.bind(on_add_ship=self.on_add_ship)
        game.bind(on_remove_ship=self.on_remove_ship)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self._background = Image(
            source=IMAGES_PATH.format('background.zip'),
            anim_delay=1
        )
        self._background.size = self._background.texture_size

        self._hp_bar = Image(pos=(10, WINDOW_HEIGHT - 80), source=ATLAS_PATH.format('100'))
        self._hp_bar.size = self._hp_bar.texture_size

        self._score = Label(pos=(950, 700), text=f'Score:   0', font_size=75)

    def show_game(self, running):
        Animation.cancel_all(self)
        self.canvas.clear()

        if not running:
            return

        self.add_widget(self._background)

        with self.canvas:
            birds = Image(
                source=IMAGES_PATH.format('birds.zip'),
                pos=(Window.width, 400),
                anim_delay=1
            )
            birds.size = birds.texture_size

            up_down = (Animation(y=375, d=5, t=self._sin_transition) +
                       Animation(y=425, d=5, t=self._sin_transition))
            up_down.repeat = True
            bird_animation = Animation(x=-birds.width, d=30) & up_down
            bird_animation.start(birds)

            bird_animation.bind(on_complete=self.on_birds_complete)

            self._game.mirror.shape = Image(
                pos=(150, 260),
                source=ATLAS_PATH.format(f'{self._game.mirror.id}-{self._game.mirror.state}')
            )
            self._game.mirror.shape.size = self._game.mirror.shape.texture_size

            self.canvas.add(self._game.sun_rays.color)
            self.canvas.add(self._game.sun_rays)

            self.canvas.add(self._game.death_rays.color)
            self.canvas.add(self._game.death_rays)

        self.add_widget(self._hp_bar)
        self.add_widget(self._score)

    def on_island_health_change(self, game, value):
        health = math.ceil(value / 10) * 10
        self._hp_bar.source = ATLAS_PATH.format(health)

    def on_add_ship(self, game, ship):
        ship.shape = ShipView(
            ship,
            source=ATLAS_PATH.format(ship.id),
            pos=(WINDOW_WIDTH, LANE_BOUNDS[ship.lane_id][1])
        )
        self.redraw_ships()

    def on_remove_ship(self, game, ship):
        ship.shape.clear_widgets()
        self.remove_widget(ship.shape)
        game.score += 1

    def redraw_ships(self):
        for lane in self._game.ship_lanes:
            for ship in lane:
                self.remove_widget(ship.shape)

        for lane in self._game.ship_lanes[::-1]:
            for ship in lane:
                self.add_widget(ship.shape)

    @staticmethod
    def _sin_transition(progress):
        return math.sin(progress * math.pi)

    @staticmethod
    def on_birds_complete(animation, birds):
        birds.pos = (Window.width, 500)
        delay = randint(10, 30)
        Clock.schedule_once(lambda dt: animation.start(birds), delay)

    def on_mirror_state_change(self, obj, value):
        self._game.mirror.shape.source = ATLAS_PATH.format(f'{self._game.mirror.id}-{value}')
        self._game.sun_rays.trace(point = LIGHT_SOURCE_POS, surface = self._game.mirror.mirror_axis)
        self._game.death_rays.trace(point = Vector(600, LANE_BOUNDS[self._game.mirror.state][1]), surface = self._game.mirror.mirror_axis)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, key_code, text, modifiers):
        action = KEY_MAPPING.get(key_code[1])
        if action is None:
            return True

        return self._game.process_action(action)

    def on_score_change(self, obj, value):
        Logger.debug(f'New score: {value}')
        self._score.text = f'Score: {value:3}'
