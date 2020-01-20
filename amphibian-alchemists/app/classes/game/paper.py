from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class PaperScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(
            lambda dt: setattr(
                self.ids.input_paper.recycle_view, "data", self.input_data()
            )
        )

    def input_data(self):
        print("WORKED!")
        return [{"text": "DATA!!!!"} for x in range(100)]
