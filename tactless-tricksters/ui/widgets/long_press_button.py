# Kivy imports
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.button import Button

import time


Builder.load_string('''
<LongpressButton>:
    id: tap_button
    valign: 'center'
    halign: 'center'
    icon: 'record'
    text: 'Tap Here'
    size: [dp(56), dp(56)]
    bg_color: app.theme_cls.primary_color
    text_color: [1, 1, 1, 1]
    long_press_dur : app.util.morse_helper.long_press_dur
    short_press_dur : app.util.morse_helper.short_press_dur
    long_pause_dur : app.util.morse_helper.long_pause_dur
    short_pause_dur : app.util.morse_helper.short_pause_dur

''')


class LongpressButton(Button):
    __events__ = ('on_long_press', 'on_short_press', 'on_long_pause', 'on_short_pause')

    long_press_dur = Factory.NumericProperty(1)
    short_press_dur = Factory.NumericProperty(1)
    long_pause_dur = Factory.NumericProperty(1)
    short_pause_dur = Factory.NumericProperty(1)

    def __init__(self, **kwargs):
        super(LongpressButton, self).__init__()
        self.text_input_cb = kwargs.get('text_input_cb')
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

    def tapped(self, morse_char):
        print(morse_char)
        self.text_input_cb([morse_char])

    def on_long_press(self, *largs):
        self.tapped('/')

    def on_short_press(self, *largs):
        self.tapped(' ')

    def on_long_pause(self, *largs):
        self.tapped('-')

    def on_short_pause(self, *largs):
        self.tapped('.')
