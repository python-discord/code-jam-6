from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MainWidget(BoxLayout):
    """Parent widget for all children"""


class ChoiceButton(Button):
    """The button which the user clicks to make the choice between two cards"""

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.register_event_type("on_card_change")

    def on_press(self):
        """
        Dispatches an event to show when the user has changed the card.
        This is useful for applying animations
        """
        super().on_press()
        self.dispatch("on_card_change")

    def on_card_change(self):
        """Default handler"""
        pass
