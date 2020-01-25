from kivy.uix.screenmanager import Screen

from .save_game import save_rotors


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
