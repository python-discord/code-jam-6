import json
from backend import path_handler

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
            print(f"\t Warning, image file is not found in path:{full_img_path}\n"
                  f"Continuing but please make sure to add image file in that path.")
        else:
            Popup(title="Image preview",
                  content=Image(source=str(full_img_path)),
                  size_hint=(None, None), size=(400, 400)).open()


class GameStatesWindow(Screen):
    with open(path_handler.get_game_state_json_path(story_name)) as f:
        game_states = json.load(f)

    def on_pre_enter(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)

        for key, value in self.game_states.items():
            btn = Button(text=f"{key} : {value}")
            layout.add_widget(btn)

        self.ids.game_states_scroll_list.add_widget(layout)

    def on_pre_leave(self):
        self.ids.game_states_scroll_list.clear_widgets()

    def wtf(self, root_ids):
        print(root_ids)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("editor.kv")


class EditorApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    EditorApp().run()
