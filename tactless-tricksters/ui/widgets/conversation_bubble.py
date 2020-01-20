from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

from kivymd.cards import MDCard
from kivymd.label import MDLabel


class ConversationBubble(ButtonBehavior, MDCard):
    def __init__(self, **kwargs):
        super(ConversationBubble, self).__init__(orientation='horizontal',
                                                 size_hint=(.6, None),
                                                 height=dp(45),
                                                 padding=(dp(5), dp(1)),
                                                 pos_hint=kwargs.get('pos_hint'))
        self.message_text = kwargs.get('message')
        self.ui_layout()
        if kwargs.get('bg_md_color'):
            with self.canvas.after:
                Color(rgba=kwargs.get('bg_md_color'))
                Rectangle(pos=self.pos, size=(Window.width, Window.height))

    def ui_layout(self):
        print(self.message_text)
        message = MDLabel(text=self.message_text, font_style='Caption')
        self.add_widget(message)
