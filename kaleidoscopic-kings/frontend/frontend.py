from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MainWidget(BoxLayout):
    """Parent widget for all children"""


class ChoiceButton(Button):
    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.register_event_type("on_card_change")

    def on_press(self):
        super().on_press()
        self.dispatch("on_card_change")

    def on_card_change(self):
        print("on_card_change")
