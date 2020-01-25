import os

from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen

from .save_game import save_rotors

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


class RotorScreen(Screen):
    def on_leave(self, *args):
        save_rotors(
            self.rotor_section.ids.first_rotor.rotor_value.text,
            self.rotor_section.ids.second_rotor.rotor_value.text,
            self.rotor_section.ids.third_rotor.rotor_value.text,
        )

    def handle_rotor_value(self, instance, rotor_value):
        gear = self.rotor_section.children[
            self.rotor_section.children.index(instance.parent.parent) - 1
        ]
        if instance.text == "+":
            rotor_value.text = self.keys[::-1][
                self.keys[::-1].index(rotor_value.text) - 1
            ]
            gear.index = (gear.index + 1) if gear.index < 9 else 0
            gear.source = f"misc/gear{gear.index}.png"
        elif instance.text == "-":
            rotor_value.text = self.keys[self.keys.index(rotor_value.text) - 1]
            gear.index = (gear.index - 1) if gear.index > 0 else 9
            gear.source = f"misc/gear{gear.index}.png"

    def load_rotors(self):
        game_id = App.get_running_app().game_id
        store = JsonStore(DATA_DIR)
        rotors = store.get(str(game_id))["current_state"]["rotors"]
        section = self.rotor_section.ids
        section.first_rotor.rotor_value.text = rotors[0]
        section.second_rotor.rotor_value.text = rotors[1]
        section.third_rotor.rotor_value.text = rotors[2]
