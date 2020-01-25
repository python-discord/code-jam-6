# Kivy imports
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

    AnchorLayout:
        anchor_x:'center'
        anchor_y:'bottom'
        padding: [dp(25), dp(25), dp(25), dp(25)]

        MDFloatingActionButton:
            id: record_button
            icon: 'record'
            size: [dp(56), dp(56)]
            md_bg_color: app.theme_cls.primary_color
            text_color: [1, 1, 1, 1]
            on_press: root.decode_audio()

    MDTextFieldRound:
        id: decode_input
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: 0.85, 0.5
        icon_left: 'key-variant'
        icon_left_dasabled: True
        icon_right: 'database-export'
        icon_callback: root.clear_input()

    MDCard:
        id: decode_card
        padding: dp(24)
        spacing: dp(24)
        orientation: 'vertical'
        size_hint: 0.85, 0.7
        pos_hint: {'top': 0.85, 'center_x': 0.5}
        elevation: 15
        md_bg_color: app.theme_cls.accent_color

        MDLabel:
            id: decode_label
            text: 'Decode Morse Code Audio'
            font_style: 'Body1'
            halign: 'center'
            size_hint: 1, .05
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]

        AudioIndicator:
            id: audio_indicator

        MDLabel:
            id: decode_output_label
            text: 'Hit record or enter Morse Code below to start decoding'
            font_style: 'Body1'
            halign: 'center'
            size_hint: 1, .05
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 1]
''')


class TappingScreen(Screen):
    training_difficulty = StringProperty("")
    decode_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TappingScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.amr = self.util.auto_morse_recognizer
        self.decode_output_label = '' # self.ids.decode_output_label
        self.record_button = '' # self.ids.record_button
        self.audio_indicator = '' #self.ids.audio_indicator

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
