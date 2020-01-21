from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class PaperScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(
            lambda dt: setattr(
                self.ids.input_paper.recycle_view, "data", self.input_data()
            )
        )

    # This only runs when the game is first opened (settings sheet)
    def input_data(self):
        input_data = [
            {"text": "Plugboard: "},
            {"text": "Rotors: "},
            {"text": "Rotor settings: "},
            {"text": "Ciphertext: "},
        ]
        return input_data

    # This paper's data is changed everytime the user comes back
    def output_data(self):
        return [{"text": "What the user has typed: "}]
