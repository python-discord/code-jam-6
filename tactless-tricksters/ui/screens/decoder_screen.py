# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# kivymd imports
from kivymd.button import MDFloatingActionButton
from kivymd.toolbar import MDToolbar
from kivymd.cards import MDCard
from kivymd.label import MDLabel
from kivymd.textfields import MDTextFieldRound

# project imports
from ui.widgets.audio_indicator import AudioIndicator

# For testing remove later
import random


class DecoderScreen(Screen):
    def __init__(self, **kwargs):
        super(DecoderScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        record_button_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom',
                                            padding=[dp(25), dp(25), dp(25), dp(25)])

        self.record_button = MDFloatingActionButton(icon='record', size=[dp(56), dp(56)])
        self.record_button.md_bg_color = App.get_running_app().theme_cls.primary_color
        self.record_button.text_color = [1, 1, 1, 1]
        self.record_button.bind(on_press=lambda x: self.decode_audio())
        record_button_anchor.add_widget(self.record_button)

        self.decode_input = MDTextFieldRound(pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.85, 0.5))
        self.decode_input.icon_left_dasabled = True
        # Moves widget out of the field of view
        self.decode_input.children[2].children[2].pos_hint = {'center_x': 500, 'center_y': 500}
        # This binds the right icon to record the input
        self.decode_input.icon_right = 'logout'
        self.decode_input.children[2].children[0].bind(on_press=lambda x: self.clear_text())

        decode_card = MDCard(padding=dp(24), spacing=dp(24), orientation='vertical',
                             size_hint_x=0.85, size_hint_y=0.7, pos_hint={'top': 0.85, 'center_x': 0.5})
        decode_label = MDLabel(text='Decode Morse Code Audio', font_style='Body1', halign='center',
                               size_hint=(1, 0.5))
        decode_label.theme_text_color = 'Custom'
        decode_label.text_color = [1, 1, 1, 1]
        decode_card.add_widget(decode_label)

        self.decode_output_label = MDLabel(text='Hit record or enter Morse Code below to start decoding',
                                           font_style='Body1', halign='center', size_hint=(1, 0.5))
        self.decode_output_label.theme_text_color = 'Custom'
        self.decode_output_label.text_color = [1, 1, 1, 1]

        self.audio_indicator = AudioIndicator()
        self.audio_indicator.size_hint = (1, 2)
        Clock.schedule_interval(self.update_audio_indicator, 0.1)

        decode_card.add_widget(self.audio_indicator)
        decode_card.add_widget(self.decode_output_label)
        decode_card.add_widget(self.decode_input)
        decode_card.md_bg_color = App.get_running_app().theme_cls.accent_color
        decode_card.elevation = 15

        self.add_widget(decode_card)
        self.add_widget(record_button_anchor)

    def update_audio_indicator(self, dt):
        if hasattr(self.audio_indicator, 'stack_width'):
            level_array = []
            for columns in range(self.audio_indicator.stack_width):
                level_array.append(random.randrange(0, self.audio_indicator.stack_height))
            self.audio_indicator.set_levels(level_array)

    def clear_text(self):
        self.decode_input.text = ''

    def decode_audio(self):
        if self.record_button.md_bg_color == App.get_running_app().theme_cls.primary_color:
            self.record_button.md_bg_color = App.get_running_app().theme_cls.error_color
            self.decode_output_label.text = 'Recording Started'
            print("Start audio recording thread")
        else:
            self.decode_output_label.text = 'Recording Stopped'
            print("Stopped audio recording thread")
            self.record_button.md_bg_color = App.get_running_app().theme_cls.primary_color

    def return_home(self):
        self.manager.current = 'welcome'
