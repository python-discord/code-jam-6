# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.app import App

# kivymd imports
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton

# project imports
from ui.widgets.nav_drawer import MyNavigationLayout
from ui.widgets.message_card import MessageCard


class MessageScreen(Screen):
    def __init__(self, **kwargs):
        super(MessageScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        layout = BoxLayout(orientation='vertical')

        self.scroll = ScrollView(do_scroll_x=False, size_hint=(1, None),
                                 size=(Window.width, Window.height))
        scroll_box = BoxLayout(orientation='vertical', size_hint_y=None,
                               padding=(dp(1), dp(60)), spacing=dp(1))
        scroll_box.bind(minimum_height=scroll_box.setter('height'))
        # Add more self.scrollbox.add_widget(MDLabel(text='')) to increase padding
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' '))
        scroll_box.add_widget(MDLabel(text=' ', size_hint=(1, 5)))

        for key in self.util.message_dict:
            temp_dict = self.util.message_dict[key]
            print(temp_dict['messages'][-1:])
            message_card = MessageCard(text_post=temp_dict['messages'][-1:][0]['text'],
                                       name=key,
                                       name_data=(key + '\n' +
                                                  temp_dict['messages'][-1:][0]['date']),
                                       swipe=True,
                                       source=temp_dict['img_source'], )
            scroll_box.add_widget(message_card)

        self.scroll.add_widget(scroll_box)
        layout.add_widget(self.scroll)

        self.add_widget(layout)

        # Add floating action button to write messages
        create_message_anchor = AnchorLayout(anchor_x='right', anchor_y='bottom',
                                             padding=[dp(25), dp(25), dp(25), dp(25)])
        create_message_btn = MDFloatingActionButton(icon='message', size=[dp(56), dp(56)])
        create_message_btn.md_bg_color = App.get_running_app().theme_cls.primary_color
        create_message_btn.theme_text_color = "Custom"
        create_message_btn.text_color = [1, 1, 1, 1]
        create_message_btn.bind(on_press=lambda x: self.switch_screens())
        create_message_anchor.add_widget(create_message_btn)
        self.add_widget(create_message_anchor)

        # Nav Bar
        self.nav_bar = MyNavigationLayout(scroll_view=self.scroll)
        self.nav_bar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.nav_bar_anchor.add_widget(self.nav_bar)
        self.add_widget(self.nav_bar_anchor)

    def switch_screens(self):
        self.manager.current = 'contact'
