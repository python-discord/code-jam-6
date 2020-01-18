# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp

from kivy.graphics import Color,Rectangle

# kivymd imports
from kivymd.button import MDFloatingActionButton
from kivymd.toolbar import MDToolbar


class DecoderScreen(Screen):
    def __init__(self, **kwargs):
        super(DecoderScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        with self.canvas:
            Color(rgba=App.get_running_app().theme_cls.accent_color)
            Rectangle(pos=self.pos, size=(Window.width, Window.height))

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title="Enigma", anchor_title='center')
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['arrow-left', lambda x: self.return_home()]]
        toolbar.elevation = 40
        toolbar_anchor.add_widget(toolbar)

        record_button_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom',
                                            padding=[dp(50), dp(50), dp(50), dp(50)])

        record_buton = MDFloatingActionButton(icon='record', size=[dp(56), dp(56)])
        record_buton.md_bg_color = App.get_running_app().theme_cls.error_color
        record_buton.text_color = [1, 1, 1, 1]
        record_buton.bind(on_press=lambda x: self.decode_audio())
        record_button_anchor.add_widget(record_buton)

        self.add_widget(toolbar_anchor)
        self.add_widget(record_button_anchor)

    def decode_audio(self):
        # TODO insert audio decoding
        pass

    def return_home(self):
        self.manager.current = 'welcome'
