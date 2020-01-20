from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.metrics import dp

from kivymd.cards import MDCard
from kivymd.label import MDLabel


class MessageCard(ButtonBehavior, MDCard):
    def __init__(self, **kwargs):
        super(MessageCard, self).__init__(orientation='horizontal',
                                          size_hint=(1.1, None), height=dp(90), pos_hint={'center_x': 0.5})
        self.orientation = 'horizontal'
        self.util = kwargs.get('util')
        self.name = kwargs.get('name')
        self.last_text = kwargs.get('last_text')
        self.date = kwargs.get('date')
        self.img_source = kwargs.get('img_source')
        self.ui_layout()

    def ui_layout(self):
        image = Image(source=self.img_source, pos_hint={'center_x': 0, 'center_y': 0.5})
        user_name_label = MDLabel(text=self.name, font_style='Body2', halign='left', valign='center')
        last_message_label = MDLabel(text=self.last_text, font_style='Caption', halign='left', valign='top')
        date_label = MDLabel(text=self.date, font_style='Caption', halign='center', valign='top')

        box_layout = BoxLayout(orientation='vertical')
        box_layout.add_widget(user_name_label)
        box_layout.add_widget(last_message_label)

        self.add_widget(image)
        self.add_widget(box_layout)
        self.add_widget(MDLabel(text=''))
        self.add_widget(MDLabel(text=''))
        self.add_widget(date_label)

    def on_press(self):
        # TODO make color change on press
        print('message pressed')
        pass

    def on_release(self):
        self.util.load_messages()
        App.get_running_app().root.content.current = 'message'






