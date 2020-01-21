import json

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import global_idmap
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from cards.main import Game, card_from_dict


class MainWidget(BoxLayout):
    pass


class CardWidget(FloatLayout):
    text = StringProperty()
    source = StringProperty()


class DataController(EventDispatcher):
    """manages global state for the app"""

    active_card = ObjectProperty()


class myApp(App):
    active_card = ObjectProperty()

    def build(self):
        global_idmap["data"] = ctl = DataController()
        with open("cards/TestCards.json") as f:
            game = Game([card_from_dict(c) for c in json.load(f)])
        ctl.active_card = game.deck.get_next_card()
        return MainWidget()


if __name__ == "__main__":
    myApp().run()
