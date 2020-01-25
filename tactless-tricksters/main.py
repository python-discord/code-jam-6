# qpy:kivy
# Kivy Imports
import gc

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import ScreenManager
from kivymd.theming import ThemeManager

from ui.screens.add_contact_screen import AddContactScreen
from ui.screens.calibration_screen import CalibrationScreen
from ui.screens.contacts_screen import ContactScreen
from ui.screens.conversation_screen import ConversationScreen
from ui.screens.decoder_screen import DecoderScreen
from ui.screens.encoder_screen import EncoderScreen
from ui.screens.listening_training_screen import ListeningScreen
from ui.screens.message_screen import MessageScreen
from ui.screens.tapping_training_screen import TappingScreen
# Project imports
from ui.screens.training_menu_screen import TrainingMenuScreen
from ui.screens.welcome_screen import WelcomeScreen
from util.utility import Utility

gc.disable()


class MainBox(FloatLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__()
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')
        self.util = Utility()
        self.content = ScreenManager()
        self.content.transition = NoTransition()

        # Place screens here
        self.content.add_widget(WelcomeScreen(name='welcome', util=self.util))
        self.content.add_widget(EncoderScreen(name='encode', util=self.util))
        self.content.add_widget(DecoderScreen(name='decode', util=self.util))
        self.content.add_widget(MessageScreen(name='message', util=self.util))
        self.content.add_widget(ConversationScreen(name='conversation', util=self.util))
        self.content.add_widget(ContactScreen(name='contact', util=self.util))
        self.content.add_widget(AddContactScreen(name='add_contact', util=self.util))
        self.content.add_widget(TrainingMenuScreen(name='training', util=self.util))
        self.content.add_widget(ListeningScreen(name='listening', util=self.util))
        self.content.add_widget(TappingScreen(name='tapping', util=self.util))
        self.content.add_widget(CalibrationScreen(name='calibration', util=self.util))
        # TODO: self.content.add_widget(CalibrationScreen(name='calibration, util=self.util))
        # # Place screens here

        self.screens.add_widget(self.content)

        self.add_widget(self.screens)


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
