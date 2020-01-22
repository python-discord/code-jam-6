import json

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import global_idmap
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

from cards.main import Game, card_from_dict


class MainWidget(BoxLayout):
    pass


class CardBoxLayout(BoxLayout):
    text = StringProperty()
    source = StringProperty()


class DataController(EventDispatcher):
    """manages global state for the app"""

    pass


Config.set("graphics", "width", "600")
Config.set("graphics", "height", "800")


class CardGameApp(App):
    active_card = ObjectProperty()

    def build(self):
        global_idmap["data"] = ctl = DataController()

        with open("cards/TestCards.json") as f:
            game = Game([card_from_dict(c) for c in json.load(f)])
        card = game.deck.get_next_card()

        # TODO replace with real state
        ctl.placeholder_art = "./assets/bonfire.png"
        ctl.active_card = card

        # TODO set these with a function reference to the game somewhere
        # TODO we can also use the same callbacks for swiping.
        ctl.choice_1_callback = lambda: print("clicked 1")
        ctl.choice_2_callback = lambda: print("clicked 2")

        return MainWidget()


if __name__ == "__main__":
    CardGameApp().run()
