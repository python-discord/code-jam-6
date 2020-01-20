# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock

# kivymd imports
from kivymd.button import MDFloatingActionButton
from kivymd.cards import MDCard
from kivymd.label import MDLabel
from kivymd.textfields import MDTextFieldRound

# project imports
from ui.widgets.audio_indicator import AudioIndicator


class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        pass