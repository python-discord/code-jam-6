from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty,
    ListProperty
)

from .dispatcher import Shell
from .termio import TerminalInput

Builder.load_file('./ancient_tech/terminal/terminal.kv')


class Terminal(BoxLayout, Shell):
    terminal_input = ObjectProperty()
    scroll_view = ObjectProperty()

    foreground_color = ListProperty((1, 1, 1, 1))
    background_color = ListProperty((0, 0, 0, 1))

    font_name = StringProperty('./ancient_tech/static/retro_font.ttf')
    font_size = NumericProperty(14)

    def __init__(self, *args, **kwargs):
        super(Terminal, self).__init__(*args, **kwargs)

    def on_output(self, output):
        self.terminal_input.on_output(output)

    def on_complete(self, output):
        self.terminal_input.on_complete(output)
        self.terminal_input.focus = True
