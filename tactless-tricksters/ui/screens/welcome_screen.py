from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivymd.button import MDRectangleFlatIconButton
from kivymd.label import MDLabel
from kivymd.toolbar import MDToolbar


class WelcomeScreen(Screen):
    texture = ObjectProperty(None)
    tex_coords = ListProperty([0, 0, 1, 0, 1, 1, 0, 1])

    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(name=kwargs.get('name'))
        Clock.schedule_once(self.texture_init, 0)

        Clock.schedule_interval(self.scroll_texture, 1/60.)
        self.util = kwargs.get('util')
        self.app = App.get_running_app()
        self.ui_layout()

    def texture_init(self, *args):
        self.canvas.before.children[-1].texture.wrap = 'repeat'

    def scroll_texture(self, dt):
        for i in range(0, 8, 2):
            self.tex_coords[i] += dt / 3.

    def ui_layout(self):
        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title="Enigma", anchor_title='center')
        toolbar.md_bg_color = self.app.get_running_app().theme_cls.primary_color
        toolbar_anchor.add_widget(toolbar)

        welcome_label = MDLabel(text='Welcome!', font_style='H4', halign='center')
        welcome_label.theme_text_color = 'Custom'
        welcome_label.text_color = [1, 1, 1, 1]


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