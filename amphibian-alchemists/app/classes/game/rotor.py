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

    def load_rotors(self):
        game_id = App.get_running_app().game_id
        store = JsonStore(DATA_DIR)
        rotors = store.get(str(game_id))["current_state"]["rotors"]
        self.rotor_section.ids.first_rotor.rotor_value.text = rotors[0]
        self.rotor_section.ids.second_rotor.rotor_value.text = rotors[1]
        self.rotor_section.ids.third_rotor.rotor_value.text = rotors[2]

    def reset_rotors(self):
        App.get_running_app().machine.set_display("AAA")
        rotors = App.get_running_app().machine.get_display()
        self.rotor_section.ids.first_rotor.rotor_value.text = rotors[0]
        self.rotor_section.ids.second_rotor.rotor_value.text = rotors[1]
        self.rotor_section.ids.third_rotor.rotor_value.text = rotors[2]
