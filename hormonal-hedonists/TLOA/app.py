from TLOA.core.constants import TITLE
from TLOA.core.game import Game
from TLOA.views import GameView

from kivy.app import App


class HormonalHedonistsApp(App):
    title = TITLE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._game = Game()
        self._view = GameView(self._game)

    def on_start(self):
        self._game.start()

    def build(self):
        return self._view
