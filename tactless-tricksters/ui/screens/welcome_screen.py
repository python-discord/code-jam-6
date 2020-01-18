# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

# KivyMD imports
from kivymd.toolbar import MDToolbar
from kivymd.cards import MDCard
from kivymd.button import MDRectangleFlatIconButton
from kivymd.label import MDLabel


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.app = App.get_running_app()

        self.ui_layout()

    def ui_layout(self):
        with self.canvas:
            Rectangle(source="ui/img/welcome_2.png", size=(Window.width, Window.height))

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title="Enigma", anchor_title='center')
        toolbar.md_bg_color = self.app.get_running_app().theme_cls.primary_color
        toolbar_anchor.add_widget(toolbar)

        welcome_label = MDLabel(text='Welcome!', font_style='H4', halign='center')
        welcome_label.theme_text_color = 'Custom'
        welcome_label.text_color = [1, 1, 1, 1]

        welcome_card = MDCard(padding=dp(24), spacing=dp(24), orientation='vertical',
                              size_hint_x=0.65, size_hint_y=0.35, pos_hint={'top': 0.8, 'center_x': 0.5})
        welcome_card.md_bg_color = App.get_running_app().theme_cls.accent_color

        decode_button = MDRectangleFlatIconButton(text=' Decode', icon='logout',
                                                  pos_hint={'center_y': 1.5, 'center_x': 0.5})

        decode_button.elevation_normal = 10
        decode_button.md_bg_color = App.get_running_app().theme_cls.primary_color
        decode_button.border_color = App.get_running_app().theme_cls.primary_color
        # Set Label to White
        decode_button.children[0].children[0].text_color = [1, 1, 1, 1]
        decode_button.children[0].children[0].font_size = 20
        # Set Icon to white
        decode_button.children[0].children[1].text_color = [1, 1, 1, 1]
        decode_button.children[0].children[1].font_size = 30
        decode_button.bind(on_press=lambda x: self.decode_screen_switch())

        encode_button = MDRectangleFlatIconButton(text=' Encode', icon='login',
                                                  pos_hint={'center_y': 1.5, 'center_x': 0.5})
        encode_button.elevation_normal = 10
        encode_button.md_bg_color = App.get_running_app().theme_cls.primary_color
        encode_button.border_color = App.get_running_app().theme_cls.primary_color
        # Set Label to White
        encode_button.children[0].children[0].text_color = [1, 1, 1, 1]
        encode_button.children[0].children[0].font_size = 20
        # Set Icon to white
        encode_button.children[0].children[1].text_color = [1, 1, 1, 1]
        encode_button.children[0].children[1].font_size = 30
        encode_button.bind(on_press=lambda x: self.encode_screen_switch())

        button_box = BoxLayout(spacing=dp(24), orientation='horizontal', pos_hint={'center_x': 0.5})
        button_box.add_widget(MDLabel(text='', font_style='H6'))
        button_box.add_widget(decode_button)
        button_box.add_widget(MDLabel(text='', font_style='H6'))
        button_box.add_widget(encode_button)
        button_box.add_widget(MDLabel(text='', font_style='H6'))

        welcome_card.add_widget(welcome_label)
        welcome_card.add_widget(MDLabel(text=''))
        welcome_card.add_widget(button_box)

        self.add_widget(toolbar_anchor)
        self.add_widget(welcome_card)

    def encode_screen_switch(self):
        self.manager.current = 'encode'

    def decode_screen_switch(self):
        self.manager.current = 'decode'

