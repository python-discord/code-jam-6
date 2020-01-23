from kivy.uix.screenmanager import Screen

from .save_game import save_rotors


class RotorScreen(Screen):
    def on_leave(self, *args):
        rotor_section = self.ids.rotor_section.ids
        save_rotors(
            rotor_section.first_rotor.ids.rotor_value.text,
            rotor_section.second_rotor.ids.rotor_value.text,
            rotor_section.third_rotor.ids.rotor_value.text
        )

    keys = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
