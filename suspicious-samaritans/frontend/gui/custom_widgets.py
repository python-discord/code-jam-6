from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty


class WidgetBackground(Widget):
    """Base widget for all widgets with a background color"""
    background_color = ListProperty([1, 1, 1, 1])


class ColorBoxLayout(BoxLayout, WidgetBackground):
    """Box layout but with background color"""
    pass


class IconButton(ButtonBehavior, Image):
    """A button with an icon"""
    icon = StringProperty("")
