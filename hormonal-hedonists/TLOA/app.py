from TLOA.core.constants import TITLE
from TLOA.core.game import Game
from TLOA.core.view import GameView

from kivy.app import App


class HormonalHedonistsApp(App):
    title = TITLE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._game = Game()
        self._view = GameView(self._game)

    def on_start(self):
        self._game.start()
        self._view.show_game()

    def build(self):
        return self._view
