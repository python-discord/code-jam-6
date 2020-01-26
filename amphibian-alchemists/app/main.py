import os

import kivy
from enigma.machine import EnigmaMachine
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivy.config import Config

kivy.require("1.11.1")
Config.set("graphics", "window_state", "maximized")

Factory.register("MainScreen", module="classes.mainscreen")
Builder.load_file("kvs/mainscreen.kv")

Factory.register("GameSelectorScreen", module="classes.gameselector")
Builder.load_file("kvs/gameselector.kv")

Factory.register("GameScreen", module="classes.game.gamescreen")
Builder.load_file("kvs/game/gamescreen.kv")

Factory.register("SettingsScreen", module="classes.settingsscreen")
Builder.load_file("kvs/settingsscreen.kv")

Factory.register("PlugboardScreen", module="classes.game.plugboard")
Builder.load_file("kvs/game/plugboard.kv")

Factory.register("RotorScreen", module="classes.game.rotor")
Builder.load_file("kvs/game/rotor.kv")

Factory.register("Paper", module="classes.game.paper")
Builder.load_file("kvs/game/paper.kv")


class UIManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()


class AncientTechApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # NOTE This is essentially a singleton
        # All global variables go here.
        self.machine = EnigmaMachine.from_key_sheet(
            rotors="I II III",
            reflector="B",
            ring_settings=[1, 20, 11],
            plugboard_settings="",
        )  # Begin instantiation. Change onload
        self.machine.set_display("AAA")
        self.game_id = None
        self.APP_DIR = os.path.dirname(os.path.abspath(__file__))

        self.keys = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]

    def build(self):
        self.title = "ENG"
        self.icon = "misc/logo.png"
        return UIManager()


if __name__ == "__main__":
    AncientTechApp().run()
