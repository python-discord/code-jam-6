# Kivy imports
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen


class TappingScreen(Screen):
    training_difficulty = StringProperty("")
    decode_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TappingScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.amr = self.util.auto_morse_recognizer
        self.decode_output_label = self.ids.decode_output_label
        self.record_button = self.ids.record_button
        self.audio_indicator = self.ids.audio_indicator

    def update_audio_indicator(self, dt):
        if hasattr(self.audio_indicator, 'stack_width'):
            level_array = [self.audio_indicator.stack_height + 1 if bit == 0 else 0 for bit in dt[-self.audio_indicator.stack_width:]]
            self.audio_indicator.set_levels(level_array)

    def update_text(self, morse_code):
        self.decode_input.text = self.decode_input.text + ''.join(morse_code)

    def clear_input(self):
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
            self.clear_input()

    def update_amr(self, kargs):
        print(kargs)
        morse_code, bit_signal = self.amr.update()
        self.update_audio_indicator(bit_signal)
        self.update_text(morse_code)

    def return_home(self):
        self.manager.current = 'welcome'
