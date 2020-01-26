from backend import path_handler

from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
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
            sound = SoundLoader.load(str(full_sound_path))
            if sound:
                print(sound.state)
                sound.play()
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
    def wtf(self):
        print("hm??!?!")


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("editor.kv")


class EditorApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    EditorApp().run()
