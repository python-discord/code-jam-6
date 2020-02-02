from kivy.uix.textinput import TextInput


class Editor(TextInput):
    def __init__(self, data: str, **kwargs):
        super().__init__(**kwargs)
        self.text = data
        self.background_color = (0, 0, 0, 0.1)
        self.foreground_color = (1, 1, 1, 1)

    def get_data(self) -> str:
        return self.text
