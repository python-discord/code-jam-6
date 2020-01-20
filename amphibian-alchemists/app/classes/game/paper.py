from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout


class PaperScreen(Screen):
    def input_data(self):
        print("WORKED!")
        return [{"text": "DATA!!!!"} for x in range(100)]
