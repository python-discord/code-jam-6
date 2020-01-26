from kivy.core.audio import SoundLoader

from backend.card_format import Card
from backend.main import load_game
from backend.main import Game
from frontend.frontend import MainWidget
from frontend.swipe import Rotater  # noqa: F401
from dataclasses import dataclass

from kivy.app import App
from kivy.config import Config
from kivy.event import EventDispatcher
from kivy.lang import global_idmap
from kivy.properties import ObjectProperty, StringProperty


class MainState:
    def __init__(self, label: str, value: float):
        self.label: str = label
        value = f"{int(value*100//2)}%"
        self.value: str = value


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
        states = [self.game.game_state.get_main_state(i) for i in range(4)]
        self.game_state = self.game_state = GameState(
            *[MainState(s.label, s.value) for s in states]
        )


class CardGameApp(App):
    def build(self):

        Config.set("graphics", "width", "900")
        Config.set("graphics", "height", "1000")
        global_idmap["data"] = ctl = DataController()
        global_idmap["all_assets"] = "./Game/"
        global_idmap["game_assets"] = "./Game/GameArt/"
        global_idmap["card_assets"] = "./Game/CardArt/"
        global_idmap["sound_assets"] = "./Game/Sounds/"
        print(global_idmap["game_assets"])
        ctl.game = game = load_game()
        ctl.active_card = game.start_game()
        ctl.set_game_state()
        sound = SoundLoader.load("./Game/Sounds/cavemen.wav")
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()
        return MainWidget()


if __name__ == "__main__":
    CardGameApp().run()
