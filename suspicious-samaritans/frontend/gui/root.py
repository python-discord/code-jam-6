from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel

from frontend.gui.custom_widgets import WidgetBackground
from frontend.gui.videocontainer import VideoContainer


class TabbedRoot(TabbedPanel, WidgetBackground):
    """Root panel to contain all tabs"""
    vid_container = ObjectProperty()
    do_default_tab = False
