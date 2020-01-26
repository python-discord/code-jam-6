from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class CardAddWindow(Screen):
    pass


class GameStatesWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("Editor.kv")


class EditorApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    EditorApp().run()
