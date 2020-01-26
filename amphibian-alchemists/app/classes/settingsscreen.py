import os

from kivy.config import Config
from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen

CONFIG_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gameconfig.json")
)
DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


class SettingsScreen(Screen):

    store = JsonStore(CONFIG_DIR)

    def on_enter(self):
        for config_name in self.ids.keys():
            if not self.store.exists(config_name):
                self.store.put(
                    config_name, value=(1 if config_name != "allow_fullscreen" else int(Config.get("graphics", "fullscreen")))
                )
            self.set_config_values(config_name)

    def set_config_values(self, config_name):
        value_to_set = {
            "allow_fullscreen": "down"
            if self.store.get(config_name)["value"] == 1
            else "normal",
            "auto_save": "down"
            if self.store.get(config_name)["value"] == 1
            else "normal",
            "background_volume": self.store.get(config_name)["value"],
            "effects_volume": self.store.get(config_name)["value"],
        }.get(config_name)

        if value_to_set in {"down", "normal"}:
            self.ids[config_name].state = value_to_set
        elif type(value_to_set) in {float, int} and (
            value_to_set >= 0 or value_to_set <= 1
        ):
            Config.write()
            self.ids[config_name].value_normalized = value_to_set

    def save_settings(self, to_save):
        new_value = {
            "allow_fullscreen": 1 if self.ids.allow_fullscreen.state == "down" else 0,
            "auto_save": 1 if self.ids.auto_save.state == "down" else 0,
            "background_volume": self.ids.background_volume.value_normalized,
            "effects_volume": self.ids.effects_volume.value_normalized,
        }.get(to_save)

        if type(new_value) in {int, float} and (new_value >= 0 or new_value <= 1):
            self.store.put(to_save, value=new_value)
            if to_save == "background_volume":
                self.manager.get_screen("main_screen").music.volume = new_value
            elif to_save == "allow_fullscreen":
                Config.set("graphics", "fullscreen", new_value)
                Config.write()

    def delete_saved_games(self, popup):
        JsonStore(DATA_DIR).clear()
        popup.dismiss()
