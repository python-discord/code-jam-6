from functools import partial

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu


class ConversationBubble(ButtonBehavior, MDCard):
    def __init__(self, **kwargs):
        super(ConversationBubble, self).__init__(orientation='horizontal',
                                                 padding=(dp(5), dp(1)),
                                                 pos_hint=kwargs.get('pos_hint'))
        self.util = kwargs.get('util')
        self._trigger_texture = Clock.create_trigger(self._update_size)
        self.label = MDLabel(size_hint_y=None)
        self.label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))

        self.size_hint = (0.6, None)
        self.md_bg_color = kwargs.get('md_bg_color')
        self.message = kwargs.get('message')
        self.label.text = self.message.text
        self.label.theme_text_color = "Custom"
        self.label.text_color = kwargs.get("text_color")
        self.add_widget(self.label)
        self.menu_items = []
        self.prompt = ''
        self.cur_sound_index = 0
        self.sound_list = []
        self.cur_sound = None
        keys = ['encode', 'decode', 'play']
        for key in keys:
            self.menu_items.append(
                {'viewclass': 'MDMenuItem',
                 'text': key,
                 'callback': partial(self.callback_for_menu_items, str(key))})
        self.bind(on_press=lambda x: MDDropdownMenu(items=self.menu_items[:],
                                                    width_mult=3,
                                                    id=key).open(self))

    def on_children(self, *_):
        for c in self.children:
            c.bind(size=self._trigger_texture)
        self._update_size()

    def _update_size(self, *_):
        temp_height = 0
        if self.size_hint_y is None:
            for c in self.children:
                temp_height += c.height
            self.height = temp_height + 10  # Add a buffer to the bottom to prevent text clipping.
        if self.size_hint_x is None:
            self.width = max(c.width for c in self.children) if self.children else 0

    def callback_for_menu_items(self, *args):
        key = args[0]
        encode = ''
        decode = ''
        if '.-' not in self.label.text:
            encode = self.util.morse_helper.text_to_morse(self.label.text)
            # self.util.morse.read(words=str(self.label.text))
        else:
            decode = self.util.morse_helper.morse_to_text(self.label.text)
            # self.util.morse.read(morse=str(self.label.text))

        if 'encode' in key.lower() and encode:
            self.label.text = encode
        if 'decode' in key.lower() and decode:
            self.label.text = decode
        if 'play' in key.lower():
            if '.-' in self.label.text:
                self.prompt = self.util.morse_helper.morse_to_text(self.label.text)
            else:
                self.prompt = self.label.text
            self.play_prompt()

    def play_prompt(self):
        self.clear_sound()
        if self.cur_sound:
            self.cur_sound_index = 999999
            self.cur_sound.stop()
        print(f"playing morse for: {self.prompt}")
        Clock.schedule_once(self.init_morse_sounds, 0)

    def init_morse_sounds(self, dt):
        self.clear_sound()

        for letter in self.prompt:
            if letter == ' ':
                self.sound_list.append('long_pause')
            else:
                self.sound_list.append(letter)
                self.sound_list.append('short_pause')

        if len(self.sound_list) > self.cur_sound_index:
            self.cur_sound = self.util.morse_helper.get_letter_as_morse_sound(self.sound_list[self.cur_sound_index])
            self.cur_sound.bind(on_stop=self.play_next_sound)
            self.cur_sound.play()

    def play_next_sound(self, dt):
        self.cur_sound_index += 1
        if len(self.sound_list) > self.cur_sound_index:
            self.cur_sound = self.util.morse_helper.get_letter_as_morse_sound(self.sound_list[self.cur_sound_index])
            self.cur_sound.bind(on_stop=self.play_next_sound)
            self.cur_sound.play()

    def clear_sound(self):
        if self.cur_sound:
            self.cur_sound.stop()
        self.cur_sound_index = 0
        self.sound_list = []
        self.cur_sound = None
  
