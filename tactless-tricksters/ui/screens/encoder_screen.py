from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color,Rectangle
from kivy.clock import Clock

# kivymd imports
from kivymd.button import MDFloatingActionButton
from kivymd.toolbar import MDToolbar
from kivymd.textfields import MDTextFieldRound
from kivymd.label import MDLabel
from kivymd.cards import MDCard

# Project imports
from ui.widgets.audio_indicator import AudioIndicator

# TODO remove after debug
import random


class EncoderScreen(Screen):
    def __init__(self, **kwargs):
        super(EncoderScreen, self).__init__(name=kwargs.get('name'))
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

        play_button_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom',
                                            padding=[dp(25), dp(25), dp(25), dp(25)])

        play_button = MDFloatingActionButton(icon='play', size=[dp(56), dp(56)])
        play_button.md_bg_color = App.get_running_app().theme_cls.primary_color# [76/255, 175/255, 80/255, 1]
        play_button.text_color = [1, 1, 1, 1]
        play_button.bind(on_press=lambda x: self.play_audio())
        play_button_anchor.add_widget(play_button)

        self.encode_input = MDTextFieldRound(pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.85, 0.5))
        self.encode_input.icon_left_dasabled = True
        # Moves widget out of the field of view
        self.encode_input.children[2].children[2].pos_hint = {'center_x': 500, 'center_y': 500}
        # This binds the right icon to record the input
        self.encode_input.icon_right = 'login'
        self.encode_input.children[2].children[0].bind(on_press=lambda x: self.encode_audio(self.encode_input.text))

        encode_card = MDCard(padding=dp(24), spacing=dp(24), orientation='vertical',
                             size_hint_x=0.85, size_hint_y=0.7, pos_hint={'top': 0.85, 'center_x': 0.5})
        encode_label = MDLabel(text='Encode Morse Code Audio', font_style='Body1', halign='center', size_hint=(1, 0.5))
        encode_label.theme_text_color = 'Custom'
        encode_label.text_color = [1, 1, 1, 1]

        self.encode_output_label = MDLabel(text='Enter text to convert to morse code', halign='center', size_hint=(1, 0.5))
        self.encode_output_label.theme_text_color = 'Custom'
        self.encode_output_label.text_color = [1, 1, 1, 1]

        self.audio_indicator = AudioIndicator()
        self.audio_indicator.size_hint = (1, 2)
        Clock.schedule_interval(self.update_audio_indicator, 0.1)

        encode_card.add_widget(encode_label)
        encode_card.add_widget(self.audio_indicator)
        encode_card.add_widget(self.encode_output_label)
        encode_card.add_widget(self.encode_input)
        encode_card.md_bg_color = App.get_running_app().theme_cls.accent_color
        encode_card.elevation = 15

        self.add_widget(encode_card)
        self.add_widget(toolbar_anchor)
        self.add_widget(play_button_anchor)

    def update_audio_indicator(self, dt):
        if hasattr(self.audio_indicator, 'stack_width'):
            level_array = []
            for columns in range(self.audio_indicator.stack_width):
                level_array.append(random.randrange(0, self.audio_indicator.stack_height))
            self.audio_indicator.set_levels(level_array)

    def encode_audio(self, text):
        # TODO insert encoding audio function
        self.util.morse.read(words=text)
        print(self.util.morse.words)
        print(self.util.morse.morse)
        self.encode_output_label.text = 'Morse Code: %s' % self.util.morse.morse
        self.encode_input.text = ''

    def play_audio(self):
        if "Morse Code" in self.encode_output_label.text:
            self.util.morse_transmit_thread()
        else:
            self.encode_output_label.text = 'Enter Text to Encode before playing'

    def return_home(self):
        self.manager.current = 'welcome'
