import os

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen

CONFIG_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gameconfig.json")
)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config_store = JsonStore(CONFIG_DIR)
        self.music = SoundLoader.load("misc/SneakySnooper.mp3")
        self.music.loop = True
        if config_store.exists("background_volume"):
            self.music.volume = config_store.get("background_volume")["value"]
        self.music.play()
