import json
from string import ascii_lowercase
from backend import path_handler, card_format

from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.config import Config
Config.set("graphics", "width", "1000")
Config.set("graphics", "height", "600")

story_name = "caveman"
with open(path_handler.get_game_state_json_path(story_name)) as f:
    _game_states = json.load(f)
with open(path_handler.get_cards_json_path(story_name)) as f:
    _game_cards = json.load(f)


def is_snake_case(string: str):
    valid = ascii_lowercase + "_"
    return all(char in valid for char in string)


class CardAddWindow(Screen):
    @classmethod
    def preview_sound(cls, sound_filename: str):
        full_sound_path = path_handler.get_game_sounds_path(story_name).joinpath(sound_filename)
        if not full_sound_path.is_file():
            print(f"\t Warning, sound file is not found in path:{full_sound_path}\n"
                  f"Continuing but please make sure to add sound file in that path.")
        else:
            # TODO pressing multiple times plays multiples times ><
            sound_file = SoundLoader.load(str(full_sound_path))
            if sound_file:
                sound_file.play()
            else:
                print("Sound file found but could not be played.")

    @classmethod
    def preview_image(cls, image_filename: str):
        full_img_path = path_handler.get_card_art_path(story_name).joinpath(image_filename)
        if not full_img_path.is_file():
            print(f"\t Image file is not found in path:{full_img_path}\n")
        else:
            Popup(title="Image preview",
                  content=Image(source=str(full_img_path)),
                  size_hint=(None, None), size=(400, 400)).open()

    def add_card(self):
        card_id = self.ids.card_id.text
        if not card_id or not is_snake_case(card_id):
            print("Card id only lowercase character plus char _ are supported.")
            return

        card_sound = self.ids.card_sound.text
        print(card_sound)  # TODO REMOVE PRECOMMIT COMPLAINED FOR NOT USING IT

        card_type = self.ids.card_type.text
        if card_type.lower() not in card_format.Card.CARD_TYPES:
            print("Invalid card type")
            return

        card_image = self.ids.card_image.text
        full_img_path = path_handler.get_card_art_path(story_name).joinpath(card_image)
        if not card_image:
            print("Invalid image input")
            return
        elif not full_img_path.is_file():
            print(f"\t Image file is not found in path:{full_img_path}\n")
            return

        card_options = self.ids.card_options.text
        try:
            card_options = json.loads(card_options)
            if len(card_options) > 2:
                print("There can be no more than 2 options!")
                return
            for option in card_options:
                # Class init will error if invalid options
                card_format.Option(**option)
        except Exception as e:
            print(f"Invalid formatted options: {e}")
            return

        card_conditions = self.ids.card_conditions.text
        if card_conditions:
            try:
                card_conditions = json.loads(card_conditions)
                for condition_name, condition_value in card_conditions.items():
                    # Class init will error if invalid value
                    card_format.GameVariable(condition_name, condition_value)
                    if condition_name not in _game_states:
                        print(f"Condition {condition_name} not in game states!")
                        return
            except Exception as e:
                print(f"Invalid formatted conditions: {e}")
                return
        else:
            card_conditions = None

        card_text = self.ids.card_text.text
        if not card_text:
            print("Invalid card text input")
            return

        """
         card_id: str
        card_type: str
        card_image: str
        text: str
        options: Union[dict, List[Option]]
        conditions: Union[dict, List[GameVariable], None] = None
        card_sound: str = None
        """
        # Class init will error if invalid type or out of range
        try:
            _ = card_format.Card(card_id, card_type, card_image, card_text, card_options,
                                 card_conditions, card_sound)
        except Exception as e:
            print(f"Can't construct card {e}")

        # TODO Use backend to generate json just by passing args to Card
        new_card = {"card_id": card_id, "card_type": card_type, "card_image": card_image,
                    "text": card_text, "options": card_options, "conditions": card_conditions,
                    "card_sound": card_sound}
        _game_cards.append(new_card)
        self.save_cards()

    def save_cards(self):
        # self.recreate_list()
        with open(path_handler.get_cards_json_path(story_name), "w") as f:
            json.dump(_game_cards, f, indent=4, sort_keys=True)


class GameStatesWindow(Screen):
    def on_pre_enter(self):
        self.recreate_list()

    def recreate_list(self):
        self.ids.game_states_scroll_list.clear_widgets()

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for key, value in _game_states.items():
            btn = Button(text=f"{key} : {value}", size_hint_y=None, height=20)
            layout.add_widget(btn)

        self.ids.game_states_scroll_list.add_widget(layout)

    def add_game_state(self, state_name_key: str, value: str):
        int_range_min, int_range_max = card_format.GameVariable.INTEGER_RANGE_INCLUDING
        float_range_min, float_range_max = card_format.GameVariable.FLOAT_RANGE_INCLUDING

        if not state_name_key or not value:
            print("Can't be empty!")
            return
        elif not is_snake_case(state_name_key):
            print("Only lowercase character plus char _ are supported.")
            return
        elif state_name_key in _game_states:
            print("Key already present!")
            return

        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif "." in value:
            try:
                value = float(value)
                if not float_range_min <= value <= float_range_max:
                    print(f"Float out of range for {state_name_key}.")
                    return
            except ValueError:
                pass
        else:
            try:
                value = int(value)
                if not int_range_min <= value <= int_range_max:
                    print(f"Int out of range for {state_name_key}.")
                    return
            except ValueError:
                print("Unknown value type.")
                return

        # Class init will error if invalid type or out of range
        try:
            card_format.GameVariable(state_name_key, value)
        except (ValueError, TypeError) as e:
            print(e)

        _game_states.update({state_name_key: value})
        self.save_game_states()

    def remove_game_state(self, state_name_key: str):
        try:
            del _game_states[state_name_key]
        except KeyError as e:
            print("No such key ", e)
            return
        self.save_game_states()

    def save_game_states(self):
        self.recreate_list()
        with open(path_handler.get_game_state_json_path(story_name), "w") as f:
            json.dump(_game_states, f, indent=4, sort_keys=True)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("editor.kv")


class EditorApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    EditorApp().run()
