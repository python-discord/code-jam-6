# Kivy imports
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
#:import MDCard kivymd.uix.card
#:import MDToolbar kivymd.uix.toolbar
#:import MDRectangleFlatIconButton kivymd.uix.button
#:import MDFloatingActionButton kivymd.uix.button
#:import MDLabel kivymd.uix.label
#:import AudioIndicator ui.widgets.audio_indicator.AudioIndicator
#:import WelcomeButton ui.widgets.welcome_button

<TappingScreen>
    decode_input: decode_input
    tapping_prompt_label: tapping_prompt_label

    MDCard:
        id: decode_card
        padding: dp(24)
        spacing: dp(24)
        orientation: 'vertical'
        size_hint: 0.85, 0.7
        pos_hint: {'top': 0.85, 'center_x': 0.5}
        elevation: 15
        md_bg_color: app.theme_cls.accent_color


        Image: 
            size_hint: 1, 1
            source: 'ui\img\morse_code_alphabet.png' 
            
        MDLabel:
            id: tapping_prompt_label
            text: root.prompt
            font_style: 'Body1'
            halign: 'center'
            size_hint: 1, .05
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]
        
        MDTextFieldRound:
            id: decode_input
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.85, 0.5
            icon_left: 'key-variant'
            icon_left_dasabled: True
            icon_right: 'database-export'
            icon_callback: root.clear_input()
        
        MDTextFieldRound:
            id: decode_input
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.85, 0.5
            icon_left: 'format-clear'
            icon_callback: root.update_text('1')
            icon_right: 'dice-5'
            icon_callback: root.new_prompt
            
        MDLabel:
            id: decode_output_label
            text: ''
            font_style: 'Body1'
            halign: 'center'
            size_hint: 1, .05
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]
        
        BoxLayout:
            anchor_x:'center'
            anchor_y:'bottom'
            padding: [dp(25), dp(25), dp(25), dp(25)]
        
            Button:
                id: tap_button
                valign: 'center'
                icon: 'record'
                text: 'Tap Here'
                size: [dp(56), dp(56)]
                bg_color: app.theme_cls.primary_color
                text_color: [1, 1, 1, 1]
                on_press: root.tapped()
''')


class TappingScreen(Screen):
    prompt = StringProperty("")
    decode_input = ObjectProperty(None)
    tapping_prompt_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TappingScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        Clock.schedule_once(self.init_tapping_screen, 0)

    def init_tapping_screen(self, dt):
        self.tapping_prompt_label = self.ids.tapping_prompt_label
        self.training_prompt_dict = self.util.training_prompt_dict
        self.amr = self.util.auto_morse_recognizer
        self.new_prompt()

    def new_prompt(self, *args):
        if self.util.training_difficulty == 'Easy':
            training_level = 'letter'
        elif self.util.training_difficulty == 'Medium':
            training_level = 'word'
        elif self.util.training_difficulty == 'Hard':
            training_level = 'sentence'
        else:
            print(f"failed to load {self.util.training_difficulty}")
            training_level = 'letter'

        prompt = random.choice(self.util.training_prompt_dict[training_level])
        self.tapping_prompt_label.text = f"Please Tap out the {training_level}: {prompt}"

    def update_text_display(self):
        try:
            words = self.util.morse(self.decode_input.text)
        except:
            words = '???'
        self.decode_input.text = words

    def update_morse_display(self, morse_code):
        self.decode_input.text = self.decode_input.text + ''.join(morse_code)
        self.update_text_display()

    def clear_input(self):
        self.decode_input.text = ''

    def tapped(self):
        print('pressed')

    def return_home(self):
        self.manager.current = 'welcome'
