import os

from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


class GameSelectorScreen(Screen):
    def on_enter(self, *args):
        print("OK")

    def populate(self):
        store = JsonStore(DATA_DIR)

