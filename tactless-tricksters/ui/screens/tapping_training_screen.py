# Kivy imports
from kivy.properties import ObjectProperty
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


class TappingScreen(Screen):
    def __init__(self, **kwargs):
        super(TappingScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.amr = self.util.auto_morse_recognizer
        self.ui_layout()
        self.training_difficulty = ''

    def ui_layout(self):
        self.decode_input = self.ids['decode_input']
        # Moves widget out of the field of view
        self.decode_input.children[2].children[2].pos_hint = {'center_x': 500, 'center_y': 500}

        print(self.amr.bits_per_frame)

    def update_audio_indicator(self, dt):
        if hasattr(self.audio_indicator, 'stack_width'):
            level_array = [self.audio_indicator.stack_height + 1 if bit == 0 else 0 for bit in dt[-self.audio_indicator.stack_width:]]
            self.audio_indicator.set_levels(level_array)

    def clear_text(self):
        self.decode_input.text = ''

    def decode_audio(self):
        if self.record_button.md_bg_color == App.get_running_app().theme_cls.primary_color:
            self.record_button.md_bg_color = App.get_running_app().theme_cls.error_color
            self.decode_output_label.text = 'Recording Started'
            print("Start audio recording thread")
            self.amr.start()
            Clock.schedule_interval(self.update_amr, self.amr.frame_rate)

        else:
            self.decode_output_label.text = 'Recording Stopped'
            print("Stopped audio recording thread")
            self.record_button.md_bg_color = App.get_running_app().theme_cls.primary_color
            Clock.unschedule(self.update_amr)
            self.amr.stop()
            self.clear_text()

    def update_amr(self, kargs):
        print(kargs)
        morse_code, bit_signal = self.amr.update()
        self.update_audio_indicator(bit_signal)
        self.update_text(morse_code)

    def update_text(self, morse_code):
        self.decode_input.text = self.decode_input.text + ''.join(morse_code)

    def return_home(self):
        self.manager.current = 'welcome'
