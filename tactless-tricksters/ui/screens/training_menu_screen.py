from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.button import MDRectangleFlatIconButton


class WelcomeButton(MDRectangleFlatIconButton):
    """Simple buttons"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._change_color)

    def _change_color(self, _):
        """Workaround to access children in this kivymd widget"""
        # Set Label to White
        self.children[0].children[0].text_color = [1, 1, 1, 1]
        self.children[0].children[0].font_size = 20
        # Set Icon to white
        self.children[0].children[1].text_color = [1, 1, 1, 1]
        self.children[0].children[1].font_size = 30


class TrainingMenuScreen(Screen):

    def __init__(self, **kwargs):
        super(TrainingMenuScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
