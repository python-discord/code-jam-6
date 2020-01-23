from backend.card_format import Card
from backend.main import Game

from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
from kivy.properties import StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


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
    """Manages global state for the app"""

    active_card: Card = ObjectProperty(rebind=True)
    active_text = StringProperty()
    game: Game = ObjectProperty()
    assets_loc = StringProperty("assets/")

    def choice_handler(self, choice):
        """Used to update state for the app when the user makes a choice"""
        if choice == "1" or len(self.active_card.options) == 1:
            outcome = self.active_card.options[0].get_outcome()
            self.active_card = self.game.take_turn(outcome)
            self.active_text = self.active_card.card_id
        else:
            outcome = self.active_card.options[0].get_outcome()
            self.active_card = self.game.take_turn(outcome)
            self.active_text = self.active_card.card_id

    def get_active_card(self):
        return self.active_card
