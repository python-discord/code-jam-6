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
    user_text_field: user_text_field
    tapping_prompt_label: tapping_prompt_label
    decode_output_label: decode_output_label
    tap_button: play_button

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
            id: morse_alphabet
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
            id: user_text_field
            hint_text: 'translate the morse that you heard here'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.85, 0.5
            icon_left: 'close-circle'
            icon_right: 'send'
            icon_callback: root.check_answer

        MDLabel:
            id: decode_output_label
            text: ''
            font_style: 'Body1'
            halign: 'center'
            size_hint: 1, .05
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]

        BoxLayout:
            rows: 2
            padding: [dp(25), dp(25), dp(25), dp(25)]

            Button:
                id: play_button
                text: 'Play Morse Code Again'
                size: [dp(56), dp(56)]
                bg_color: app.theme_cls.primary_color
                text_color: [1, 1, 1, 1]
                on_press: root.play_prompt()

            Button:
                id: play_button
                text: 'Play New Morse Code'
                size: [dp(56), dp(56)]
                bg_color: app.theme_cls.primary_color
                text_color: [1, 1, 1, 1]
                on_press: root.play_new_prompt()
''')


class ListeningScreen(Screen):
    prompt = StringProperty("")
    user_text_field = ObjectProperty(None)
    decode_output_label = ObjectProperty(None)
    tapping_prompt_label = ObjectProperty(None)
    play_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListeningScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')

    def on_enter(self):
        Clock.schedule_once(self.init_listening_screen, 0)
        self.sound_list = []
        self.cur_sound_index = 0
        self.cur_sound = None

    def init_listening_screen(self, dt):
        self.tapping_prompt_label = self.ids.tapping_prompt_label
        self.user_text_field.children[2].children[2].disabled = False
        self.user_text_field.children[2].children[2].bind(on_press=lambda x: self.clear_input())
        self.training_prompt_dict = self.util.training_prompt_dict
        self.decode_output_label.text = "^-- click on the left button to clear" \
                                        " and the right button for new prompt --^\n" \
                                        "v---click here to replay audio and here" \
                                        " to play new audio --v"
        self.play_new_prompt()

    def check_answer(self, *args):
        user_input = self.user_text_field.text.lower()
        if self.prompt == user_input:
            self.decode_output_label.text = "You got it right!"
        else:
            self.decode_output_label.text = "nope you got it wrong!"

    def play_prompt(self):
        if self.cur_sound:
            self.cur_sound_index = 9999
            self.cur_sound.stop()

        print(f"playing morse for: {self.prompt}")
        Clock.schedule_once(self.init_morse_sounds, 0)

    def init_morse_sounds(self, dt):
        self.cur_sound_index = 0
        self.sound_list = []

        for letter in self.prompt:
            if letter == ' ':
                self.sound_list.append('long_pause')
            else:
                self.sound_list.append(letter)
                self.sound_list.append('short_pause')

        if len(self.sound_list) > self.cur_sound_index:
            letter_char_sound = self.sound_list[self.cur_sound_index]
            self.cur_sound = self.util.morse_helper.get_letter_as_morse_sound(letter_char_sound)
            self.cur_sound.bind(on_stop=self.play_next_sound)
            self.cur_sound.play()

    def play_next_sound(self, dt):
        self.cur_sound_index += 1
        if len(self.sound_list) > self.cur_sound_index:
            letter_char_sound = self.sound_list[self.cur_sound_index]
            self.cur_sound = self.util.morse_helper.get_letter_as_morse_sound(letter_char_sound)
            self.cur_sound.bind(on_stop=self.play_next_sound)
            self.cur_sound.play()

    def play_new_prompt(self):
        self.clear_input()
        if self.util.training_difficulty in ['Easy', 'Medium', 'Hard']:
            if self.util.training_difficulty == 'Easy':
                training_level = 'letter'
            elif self.util.training_difficulty == 'Medium':
                training_level = 'word'
            else:
                training_level = 'sentence'
            self.prompt = random.choice(self.util.training_prompt_dict[training_level])
            self.tapping_prompt_label.text = f"Please translate the morse code " \
                                             f"({training_level}) being played"
        else:
            print(f"failed to load {self.util.training_difficulty}")

        self.play_prompt()

    def clear_input(self):
        self.user_text_field.text = ''
        self.decode_output_label.text = ""

    def return_menu(self):
        self.manager.current = 'training'

    def return_home(self):
        self.manager.current = 'welcome'
