import datetime
from dataclasses import dataclass

from kivy.event import EventDispatcher

from backend.card_format import Card
from frontend.frontend import MainWidget
from backend.main import load_game, Game

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.config import Config
from kivy.lang import global_idmap


@dataclass
class MainState:
    label: str
    value: str


@dataclass
class GameState:
    main_state_1: MainState
    main_state_2: MainState
    main_state_3: MainState
    main_state_4: MainState


class DataController(EventDispatcher):
    """Manages global state for the app"""

    active_card: Card = ObjectProperty(rebind=True)
    game_state = ObjectProperty(rebind=True)
    game: Game = ObjectProperty()
    assets_loc = StringProperty("assets/")

    def choice_handler(self, choice):
        """Used to update state for the app when the user makes a choice"""
        if choice == "1" or len(self.active_card.options) == 1:
            outcome = self.active_card.options[0].get_outcome()
            self.active_card = self.game.take_turn(outcome)
        else:
            outcome = self.active_card.options[0].get_outcome()
            self.active_card = self.game.take_turn(outcome)

        self.set_game_state()

    def set_game_state(self):
        """
        Sets teh states for the 4 main player states. Currently uses dud values til the
        backend version is done
        """
        self.game_state = self.game_state = GameState(
            *[
                MainState(str(datetime.datetime.now()), "a"),
                MainState(str(datetime.datetime.now()), "b"),
                MainState(str(datetime.datetime.now()), "c"),
                MainState(str(datetime.datetime.now()), "d"),
            ]
        )


class CardGameApp(App):
    def build(self):
        Config.set("graphics", "width", "900")
        Config.set("graphics", "height", "900")

        global_idmap["data"] = ctl = DataController()

        ctl.game = game = load_game()
        ctl.active_card = game.start_game()
        ctl.set_game_state()
        return MainWidget()


if __name__ == "__main__":
    CardGameApp().run()
