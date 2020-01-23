from kivy.event import EventDispatcher

from backend.card_format import Card
from frontend.frontend import MainWidget
from backend.main import load_game, Game

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.config import Config
from kivy.lang import global_idmap


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
