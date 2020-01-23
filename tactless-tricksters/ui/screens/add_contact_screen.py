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

# For testing remove later
import random


class AddContactScreen(Screen):
    def __init__(self, **kwargs):
        super(AddContactScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.nav_bar = kwargs.get('nav_bar')
        self.add_widget(self.nav_bar)
        self.ui_layout()

    def ui_layout(self):
        pass