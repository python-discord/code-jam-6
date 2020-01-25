from kivy.clock import Clock
from kivy.app import App

from kivymd.uix.button import MDRectangleFlatIconButton


class WelcomeButton(MDRectangleFlatIconButton):
    """Simple buttons"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._change_color)
        self.elevation_normal = 10
        self.md_bg_color = App.get_running_app().theme_cls.primary_color
        self.md_border_color: App.get_running_app().theme_cls.primary_color
        self.pos_hint = {'center_y': 1.5, 'center_x': 0.5}

    def _change_color(self, _):
        """Workaround to access children in this kivymd widget"""
        # Set Label to White
        self.children[0].children[0].text_color = [1, 1, 1, 1]
        self.children[0].children[0].font_size = 20
        # Set Icon to white
        self.children[0].children[1].text_color = [1, 1, 1, 1]
        self.children[0].children[1].font_size = 30
