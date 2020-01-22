import json
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import global_idmap
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from backend.main import Game, Card


class MainWidget(Widget):
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
        with open("backend/data/example_game_cards.json") as f:
            _cards = [Card(**card_dict) for card_dict in json.load(f)]
        with open("backend/data/example_game_states.json") as f:
            _game_states = json.load(f)

        game = Game(_cards, _game_states)

        global_idmap["data"] = ctl = DataController()
        ctl.active_card = game.start_game()
        return MainWidget()


if __name__ == "__main__":
    myApp().run()
