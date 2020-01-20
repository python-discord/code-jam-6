# qpy:kivy
# Kivy Imports
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import NoTransition
from kivymd.theming import ThemeManager
from kivy.app import App


# Project imports
from ui.screens.welcome_screen import WelcomeScreen
from ui.screens.encoder_screen import EncoderScreen
from ui.screens.decoder_screen import DecoderScreen
from ui.screens.message_screen import MessageScreen
from ui.screens.conversation_screen import ConversationScreen
from util.utility import Utility
from ui.widgets.nav_drawer import MyNavigationLayout


class MainBox(FloatLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__()
        self.nav_bar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.nav_bar = MyNavigationLayout()
        self.nav_bar_anchor.add_widget(self.nav_bar)
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')
        self.util = Utility()
        self.content = ScreenManager()
        self.content.transition = NoTransition()

        # Place screens here
        self.content.add_widget(ConversationScreen(name='conversation', util=self.util))
        self.content.add_widget(WelcomeScreen(name='welcome', util=self.util))
        self.content.add_widget(EncoderScreen(name='encode', util=self.util))
        self.content.add_widget(DecoderScreen(name='decode', util=self.util))
        self.content.add_widget(MessageScreen(name='message', util=self.util))
        # Place screens here

        self.screens.add_widget(self.content)

        self.add_widget(self.screens)
        self.add_widget(self.nav_bar_anchor)


class MainApp(App):
    # Change APP colors here
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Teal'
    theme_cls.primary_hue = '300'
    theme_cls.accent_palette = 'Gray'
    theme_cls.accent_hue = '800'
    theme_cls.theme_style = 'Dark'
    accent_color = [255/255, 64/255, 129/255, 1]

    def build(self):
        return MainBox()


if __name__ == "__main__":
    MainApp().run()
