import inspect
import json
from os.path import extsep, exists, splitext

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import global_idmap, Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout

from cards.main import Game, card_from_dict


class MainWidget(GridLayout):
    pass


class StatusBar(BoxLayout):
    pass


class CardWidget(BoxLayout):
    """Widget that contains a card, its art, and buttons to make the relevant choices"""

    pass


class CardBoxLayout(BoxLayout):
    """Standard box layout with a stone tablet as a background"""

    source = StringProperty()


class DataController(EventDispatcher):
    """manages global state for the app"""


def load_kv():
    """
    This magical function lookup module name, and load the kv file
    with the same name (in the same directory)
    """
    filename = inspect.currentframe().f_back.f_code.co_filename
    f = extsep.join((splitext(filename)[0], "kv"))
    print(f)
    if exists(f) and f not in Builder.files:
        Builder.load_file(f)


class CardGameApp(App):
    active_card = ObjectProperty()

    def build(self):
        Config.set("graphics", "width", "900")
        Config.set("graphics", "height", "900")
        load_kv()

        global_idmap["data"] = ctl = DataController()
        with open("../cards/TestCards.json") as f:
            game = Game([card_from_dict(c) for c in json.load(f)])
        card = game.deck.get_next_card()

        # TODO replace with real state
        ctl.placeholder_art = "../assets/bonfire_icon.png"
        ctl.active_card = card

        # TODO set these with a function reference to the game somewhere
        # TODO we can also use the same callbacks for swiping.
        ctl.choice_1_callback = lambda: print("clicked 1")
        ctl.choice_2_callback = lambda: print("clicked 2")

        return MainWidget()


if __name__ == "__main__":
    CardGameApp().run()
