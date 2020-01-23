from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.clock import Clock

from kivymd.cards import MDCard
from kivymd.label import MDLabel
from kivymd.menus import MDMenu, MDDropdownMenu

from functools import partial

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
        keys = ['encode', 'decode', 'play']
        for key in keys:
            self.menu_items.append({'viewclass': 'MDMenuItem','text': key,'callback': partial(self.callback_for_menu_items,str(key))})
        self.bind(on_press=lambda x: MDDropdownMenu(items=self.menu_items[:], width_mult=3, id=key).open(self))

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
        if '.-' not in self.label.text:
            self.util.morse.read(words=str(self.label.text))
        else:
            self.util.morse.read(morse=str(self.label.text))

        if 'encode' in key.lower():
            self.label.text = self.util.morse.morse
        if 'decode' in key.lower():
            self.label.text = self.util.morse.words
        if 'play' in key.lower():
            self.util.morse_transmit_thread()
