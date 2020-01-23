from frontend.frontend import DataController, MainWidget
from backend.main import load_game

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.lang import global_idmap


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
