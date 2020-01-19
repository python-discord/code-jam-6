from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color,Rectangle

# kivymd imports
from kivymd.button import MDFloatingActionButton
from kivymd.toolbar import MDToolbar
from kivymd.textfields import MDTextFieldRound
from kivymd.label import MDLabel


class EncoderScreen(Screen):
    def __init__(self, **kwargs):
        super(EncoderScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        with self.canvas:
            Color(rgba=App.get_running_app().theme_cls.accent_color)
            Rectangle(pos=self.pos, size=(Window.width, Window.height))

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title="Enigma", anchor_title='center')
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['arrow-left', lambda x: self.return_home()]]
        toolbar.elevation = 40
        toolbar_anchor.add_widget(toolbar)

        play_button_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom',
                                            padding=[dp(50), dp(50), dp(50), dp(50)])

        play_button = MDFloatingActionButton(icon='play', size=[dp(56), dp(56)])
        play_button.md_bg_color = [76/255, 175/255, 80/255, 1]
        play_button.text_color = [1, 1, 1, 1]
        play_button.bind(on_press=lambda x: self.play_audio())
        play_button_anchor.add_widget(play_button)

        box_layout = BoxLayout(orientation='vertical')

        self.encode_input = MDTextFieldRound(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.encode_input.icon_left_dasabled = True
        # Moves widget out of the field of view
        self.encode_input.children[2].children[2].pos_hint = {'center_x': 500, 'center_y': 500}
        # This binds the right icon to record the input
        self.encode_input.icon_right = 'login'
        self.encode_input.children[2].children[0].bind(on_press=lambda x: self.encode_audio(self.encode_input.text))

        box_layout.add_widget(MDLabel(text=''))
        box_layout.add_widget(MDLabel(text=''))
        box_layout.add_widget(MDLabel(text=''))
        box_layout.add_widget(self.encode_input)
        box_layout.add_widget(MDLabel(text=''))

        self.add_widget(box_layout)
        self.add_widget(toolbar_anchor)
        self.add_widget(play_button_anchor)

    def encode_audio(self, text):
        # TODO insert encoding audio function
        print(text)
        self.encode_input.text = ''


    def play_audio(self):
        # TODO insert audio encoding
        pass

    def return_home(self):
        self.manager.current = 'welcome'
