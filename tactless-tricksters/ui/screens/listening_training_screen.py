# Kivy imports
import random
import time

from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class LongpressButton(Button):
    __events__ = ('on_long_press', 'on_short_press', 'on_long_pause', 'on_short_pause')

    long_press_dur = Factory.NumericProperty(1)
    short_press_dur = Factory.NumericProperty(1)
    long_pause_dur = Factory.NumericProperty(1)
    short_pause_dur = Factory.NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_release_time = None
        self.last_press_time = None

    def on_release(self):
        self.last_release_time = time.time()
        press_duration = time.time() - self.last_press_time
        if press_duration >= self.long_press_dur:
            self.dispatch('on_long_press')
        else:
            self.dispatch('on_short_press')

    def on_press(self):
        self.last_press_time = time.time()
        if self.last_release_time is not None:
            pause_duration = time.time() - self.last_release_time
            if pause_duration >= self.long_pause_dur:
                print('long_pause')
                self.dispatch('on_long_pause')
            elif pause_duration >= self.short_pause_dur:
                print('short_pause')
                self.dispatch('on_short_pause')

    def set_morse_timing(self, morse_timing_dict):
        self.long_press_dur = morse_timing_dict['long_press_dur']
        self.short_press_dur = morse_timing_dict['short_press_dur']
        self.long_pause_dur = morse_timing_dict['long_pause_dur']
        self.short_pause_dur = morse_timing_dict['short_pause_dur']

    def on_long_press(self, *largs):
        pass

    def on_short_press(self, *largs):
        pass

    def on_long_pause(self, *largs):
        pass

    def on_short_pause(self, *largs):
        pass


Builder.load_string('''
#:import MDCard kivymd.uix.card
#:import MDToolbar kivymd.uix.toolbar
#:import MDRectangleFlatIconButton kivymd.uix.button
#:import MDFloatingActionButton kivymd.uix.button
#:import MDLabel kivymd.uix.label
#:import AudioIndicator ui.widgets.audio_indicator.AudioIndicator
#:import WelcomeButton ui.widgets.welcome_button

<ListeningScreen>
    decode_morse: decode_morse
    decode_text: decode_text
    tapping_prompt_label: tapping_prompt_label
    decode_output_label: decode_output_label
    tap_button: tap_button
    
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        
        MDToolbar:
            title: 'Listening Training'
            anchor_title: 'center'
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["arrow-left", lambda x: root.return_menu()]]
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
            source: 'ui/img/morse_code_alphabet.png' 

        MDLabel:
            id: tapping_prompt_label
            text: root.prompt
            font_style: 'Body1'
            halign: 'center'
            size_hint: 1, .05
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]

        MDTextFieldRound:
            id: decode_text
            icon_type: 'without'
            hint_text: 'The text of your morse will be displayed here'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.85, 0.5

        MDTextFieldRound:
            id: decode_morse
            hint_text: 'Your morse will be displayed here'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.85, 0.5
            icon_left: 'close-circle'
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

            LongpressButton:
                id: tap_button
                valign: 'center'
                icon: 'record'
                text: 'Tap Here'
                size: [dp(56), dp(56)]
                bg_color: app.theme_cls.primary_color
                text_color: [1, 1, 1, 1]
                on_short_press: root.tapped('.')
                on_long_press: root.tapped('-')
                on_short_pause: root.tapped(' ')
                on_long_pause: root.tapped('/')
                long_press_dur : app.util.morse_helper.long_press_dur
                short_press_dur : app.util.morse_helper.short_press_dur
                long_pause_dur : app.util.morse_helper.long_pause_dur
                short_pause_dur : app.util.morse_helper.short_pause_dur
''')


class ListeningScreen(Screen):
    prompt = StringProperty("")
    decode_morse = ObjectProperty(None)
    decode_text = ObjectProperty(None)
    decode_output_label = ObjectProperty(None)
    tapping_prompt_label = ObjectProperty(None)
    tap_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListeningScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')

    def on_enter(self):
        Clock.schedule_once(self.init_tapping_screen, 0)

    def init_tapping_screen(self, dt):
        self.tapping_prompt_label = self.ids.tapping_prompt_label
        self.decode_morse.children[2].children[2].disabled = False
        self.decode_morse.children[2].children[2].bind(on_press=lambda x: self.clear_input())
        self.training_prompt_dict = self.util.training_prompt_dict
        self.decode_output_label.text = "^-- click on the left button to clear" \
                                        " and the right button for new prompt --^"
        self.decode_text = self.ids.decode_text

    def new_prompt(self, *args):
        self.clear_input()
        self.ids.decode_output_label.text = ""
        if self.util.training_difficulty in ['Easy', 'Medium', 'Hard']:
            if self.util.training_difficulty == 'Easy':
                training_level = 'letter'
            elif self.util.training_difficulty == 'Medium':
                training_level = 'word'
            else:
                training_level = 'sentence'
            self.prompt = random.choice(self.util.training_prompt_dict[training_level])
            self.tapping_prompt_label.text = f"Please Tap out the {training_level}: {self.prompt}"
        else:
            print(f"failed to load {self.util.training_difficulty}")

    def update_text_display(self):
        user_input = self.util.morse_helper.morse_to_text(self.decode_morse.text)
        self.decode_text.text = user_input
        if self.prompt == user_input:
            self.ids.decode_output_label.text = "You got it! click dice icon to do next"

    def update_morse_display(self, morse_code):
        self.decode_morse.text = self.decode_morse.text + ''.join(morse_code)
        self.update_text_display()

    def clear_input(self):

        self.decode_morse.text = ''
        self.decode_text.text = ''
        self.ids.decode_output_label.text = ""

    def tapped(self, morse_char):
        print(morse_char)
        self.update_morse_display([morse_char])

    def return_menu(self):
        self.manager.current = 'training'

    def return_home(self):
        self.manager.current = 'welcome'
