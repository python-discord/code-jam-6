from kivy.properties import StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class MainWidget(GridLayout):
    pass


class StatusBar(BoxLayout):
    pass


class CardWidget(BoxLayout):
    """
    Widget that contains a card, art, and buttons to make the relevant choices
    """

    pass


class CardBoxLayout(BoxLayout):
    """Standard box layout with a stone tablet as a background"""

    source = StringProperty()
