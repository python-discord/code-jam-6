from TLOA.core.game import Game
from TLOA.core.constants import ATLAS_PATH

from kivy.graphics import Rectangle
from kivy.uix.widget import Widget


class GameView(Widget):
    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)
        self._game = game

        with self.canvas:
            game.mirror.shape = Rectangle(
                source=ATLAS_PATH.format(f'mirror_cannon/{self._game.mirror.state}'))

        game.mirror.bind(state=self.on_mirror_state_change)

    def on_mirror_state_change(self, obj, value):
        self._game.mirror.shape.source = ATLAS_PATH.format(f'mirror_cannon/{value}')
