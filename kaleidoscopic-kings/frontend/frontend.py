import json

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import global_idmap
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout

from backend.card_format import Card
from backend.main import Game


class MainWidget(GridLayout):
    pass


class StatusBar(BoxLayout):
    pass


class CardWidget(BoxLayout):
    """
    Widget that contains a card, art, and buttons to make the relevant choices
    """

    pass


class CardBoxLayout(BoxLayout):
    """Standard box layout with a stone tablet as a background"""

    source = StringProperty()


class DataController(EventDispatcher):
    """manages global state for the app"""

    active_card: Card = ObjectProperty(rebind=True)
    active_text = StringProperty()
    game: Game = ObjectProperty()

    def choice_handler(self, choice):
        """Used to update state for the app when the user makes a choice"""
        if choice == "1" or len(self.active_card.options) == 1:
            outcome = self.active_card.options[0].get_outcome()
            self.active_card = self.game.take_turn(outcome)
            self.active_text = self.active_card.card_id
            print(f"User is making choice {choice} on card {self.active_card}")
        else:
            outcome = self.active_card.options[0].get_outcome()
            self.active_card = self.game.take_turn(outcome)
            self.active_text = self.active_card.card_id
            print(f"User is making choice {choice} on card {self.active_card}")

    def get_active_card(self):
        return self.active_card


def load_game() -> Game:
    """Loads the backend and returns a game object"""
    with open("../backend/data/example_game_cards.json") as f:
        _cards = [Card(**card_dict) for card_dict in json.load(f)]
    with open("../backend/data/example_game_states.json") as f:
        _game_states = json.load(f)
    return Game(_cards, _game_states)


class CardGameApp(App):
    active_card = ObjectProperty()

    def build(self):
        Config.set("graphics", "width", "900")
        Config.set("graphics", "height", "900")

        global_idmap["data"] = ctl = DataController()

        ctl.game = game = load_game()
        ctl.active_card = game.start_game()
        return MainWidget()


if __name__ == "__main__":
    CardGameApp().run()
