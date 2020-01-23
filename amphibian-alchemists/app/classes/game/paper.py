import os

from kivy.app import App
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.relativelayout import RelativeLayout

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


class Paper(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(
            lambda dt: setattr(
                self.ids.input_paper.recycle_view_input, "data", self.input_data()
            ), 1
        )

    # This only runs when the game is first opened (settings sheet)
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
        current_state = game["encrypted_state"]
        plugs = current_state["plugs"]
        plug_settings = " ".join(x for x in plugs)
        rotor_settings = "I II III"
        rotors = ""
        for x in store.get(game_id)["current_state"]["rotors"]:
            if x is None:
                continue
            rotors += x

        input_data = [
            {"text": f"Plugboard:\n{plug_settings}"},
            {"text": f"Rotors:\n{rotor_settings}"},
            {"text": f"Rotor settings:\n{rotors}"},
            {"text": f"Ciphertext:\n{cipher_text}"},
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
