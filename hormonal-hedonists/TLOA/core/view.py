from random import randint

from TLOA.core.game import Game
from TLOA.core.constants import ATLAS_PATH, IMAGES_PATH, KEY_MAPPING

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock

import math


class GameView(Widget):
    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)
        self._game = game

        game.mirror.bind(state=self.on_mirror_state_change)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def show_game(self):
        Animation.cancel_all(self)
        self.canvas.clear()
        with self.canvas:
            #sky = Image(source=IMAGES_PATH.format('sky.png'))
            #sky.size = sky.texture_size

            #waves = Image(source=IMAGES_PATH.format('sea_waves.gif'))
            #waves.size = waves.texture_size
            #waves.anim_delay = 1

            #island = Image(source=IMAGES_PATH.format('island.png'))
            #island.size = island.texture_size

            background = Image(source=IMAGES_PATH.format('background.gif'))
            background.size = background.texture_size
            background.anim_delay = 1

            birds = Image(pos=(Window.width, 400), source=ATLAS_PATH.format('birds-0'))
            birds.size = birds.texture_size
            up_down = (Animation(y=350, d=5, t=self._sin_transition) +
                       Animation(y=450, d=5, t=self._sin_transition))
            up_down.repeat = True
            bird_animation = Animation(x=-birds.width, d=30) & up_down
            bird_animation.start(birds)

            bird_animation.bind(on_complete=self.on_birds_complete)

            #sun = Image(pos=(650, 530), source=ATLAS_PATH.format('sun-0'))
            #sun.size = sun.texture_size

            self._game.mirror.shape = Image(
                pos=(150, 260),
                source=ATLAS_PATH.format(f'{self._game.mirror.id}-{self._game.mirror.state}')
            )
            self._game.mirror.shape.size = self._game.mirror.shape.texture_size

    @staticmethod
    def _sin_transition(progress):
        return math.sin(progress * math.pi)

    @staticmethod
    def on_birds_complete(animation, birds):
        birds.pos = (Window.width, 500)
        delay = randint(10, 30)
        Clock.schedule_interval(lambda dt: animation.start(birds), delay)

    def on_mirror_state_change(self, obj, value):
        self._game.mirror.shape.source = ATLAS_PATH.format(f'{self._game.mirror.id}-{value}')

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, key_code, text, modifiers):
        action = KEY_MAPPING.get(key_code[1])
        if action is None:
            return True

        return self._game.process_action(action)
