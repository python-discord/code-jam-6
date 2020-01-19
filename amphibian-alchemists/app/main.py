import kivy
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition, ScreenManager

kivy.require("1.11.1")

Factory.register("MainScreen", module="classes.mainscreen")
Builder.load_file("kvs/mainscreen.kv")

Factory.register("GameScreen", module="classes.gamescreen")
Builder.load_file("kvs/game/gamescreen.kv")

Factory.register("SettingsScreen", module="classes.settingsscreen")
Builder.load_file("kvs/settingsscreen.kv")

Factory.register("Paper", module="classes.gamescreen")
Builder.load_file("kvs/game/paper.kv")

Factory.register("Plugboard", module="classes.gamescreen")
Builder.load_file("kvs/game/plugboard.kv")

Factory.register("Rotor", module="classes.gamescreen")
Builder.load_file("kvs/game/rotor.kv")


class UIManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()


class AncientTechApp(App):
    def build(self):
        self.title = "ENG"
        self.icon = "misc/logo.png"
        return UIManager()


if __name__ == "__main__":
    AncientTechApp().run()
