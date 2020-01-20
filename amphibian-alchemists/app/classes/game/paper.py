from kivy.uix.screenmanager import Screen


class PaperScreen(Screen):
    def input_data(self):
        print("WORKED!")
        return [{"text": "DATA!!!!"} for x in range(100)]
