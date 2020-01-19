from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.metrics import dp

from kivymd.cards import MDCard
from kivymd.label import MDLabel


class ConversationBubble(ButtonBehavior, MDCard):
    def __init__(self, **kwargs):
        super(ConversationBubble, self).__init__(orientation='horizontal',
                                          size_hint=(.6, None), height=dp(15), pos_hint={'center_x': 0.5})
        self.message_text = kwargs.get('message')
        self.ui_layout()

    def ui_layout(self):
        print(self.message_text)
        message = MDLabel(text=self.message_text, font_style='Caption')
        self.add_widget(message)
