from kivy.uix.screenmanager import Screen

from .save_game import save_rotors


class RotorScreen(Screen):
    def on_leave(self, *args):
        save_rotors(
            self.rotor_section.ids.first_rotor.rotor_value.text,
            self.rotor_section.ids.second_rotor.rotor_value.text,
            self.rotor_section.ids.third_rotor.rotor_value.text,
        )
