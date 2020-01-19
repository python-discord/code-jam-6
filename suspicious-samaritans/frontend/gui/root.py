from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ListProperty, StringProperty


class ColorBoxLayout(BoxLayout):
    """Box layout but with background color"""
    background_color = ListProperty([1, 1, 1, 1])


class IconButton(ButtonBehavior, Image):
    """A button with an icon"""
    icon = StringProperty("")


class RootLayout(ColorBoxLayout):
    """Root widget for the entire screen"""
    pass
