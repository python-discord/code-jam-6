# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock

# kivymd imports
from kivymd.button import MDFloatingActionButton
from kivymd.cards import MDCard
from kivymd.label import MDLabel
from kivymd.textfields import MDTextFieldRound

# project imports
from ui.widgets.message_card import MessageCard


class MessageScreen(Screen):
    def __init__(self, **kwargs):
        super(MessageScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        layout = BoxLayout(orientation='vertical')

        scroll = ScrollView(do_scroll_x=False, size_hint=(1, None), size=(Window.width, Window.height))
        scroll_box = BoxLayout(orientation='vertical', size_hint_y=None, padding=(dp(1), dp(60)), spacing=dp(1))
        scroll_box.bind(minimum_height=scroll_box.setter('height'))
        # Add more self.scrollbox.add_widget(MDLabel(text='')) to increase padding
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' ', size_hint=(1, 5)))

        for key in self.util.message_dict:
            temp_dict = self.util.message_dict[key]
            print(temp_dict['messages'][-1:])
            message_card = MessageCard(util=self.util,
                                       name=key,
                                       last_text=temp_dict['messages'][-1:][0],
                                       date=temp_dict['date'],
                                       img_source=temp_dict['img_source']
                                       )
            scroll_box.add_widget(message_card)

        scroll.add_widget(scroll_box)
        layout.add_widget(scroll)
        self.add_widget(layout)
