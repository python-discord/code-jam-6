import os

from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.relativelayout import RelativeLayout

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


class Paper(RelativeLayout):
    # Constantly runs with schedule_interval to avoid game interference
    def input_data(self):
        store = JsonStore(DATA_DIR)
        game_id = str(App.get_running_app().game_id)
        if game_id == "None":
            return [
                {"text": "Plugboard: "},
                {"text": "Rotors: "},
                {"text": "Rotor settings: "},
                {"text": "Ciphertext: "},
            ]
        game = store.get(game_id)
        cipher_text = game["ciphered_text"]
        encrypted_state = game["encrypted_state"]
        plugs = encrypted_state["plugs"]
        plug_settings = " ".join(x for x in plugs)
        rotor_settings = "I II III"
        rotors = ""
        for i, x in enumerate(encrypted_state["rotors"]):
            if x is None:
                continue
            rotors += x
            if i % 2 == 0:
                rotors += " "

        input_data = [
            {"text": "Plugboard:"},
            {"text": plug_settings},
            {"text": "Rotors:"},
            {"text": rotors},
            {"text": "Rotor settings:"},
            {"text": rotor_settings},
            {"text": "Ciphertext:"},
            {"text": cipher_text},
        ]
        return input_data

    # This paper's data is changed everytime the user comes back
    def output_data(self):
        store = JsonStore(DATA_DIR)
        game_id = str(App.get_running_app().game_id)
        if game_id == "None":
            return [{"text": "Output:"}]
        game = store.get(game_id)
        current_output_text = game["current_output_text"]
        return [{"text": f"Output:\n{current_output_text}"}]
