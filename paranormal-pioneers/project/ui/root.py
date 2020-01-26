from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import (
    ObjectProperty, ListProperty, StringProperty,
    NumericProperty, Clock, partial
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from project.core.path import Path
from project.core.terminal import Terminal

root = Path(__file__).parent.resolve()
font = str(root / 'font.ttf')


class Shell(EventDispatcher):
    __events__ = ('on_output', 'on_complete')
    term = ObjectProperty(None)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.term = Terminal()
        self.term._prepare()

    def run_command(self, command, show_output=True, *args):
        try:
            result = self.term.parser.execute(command, self.term)
        except Exception as exc:
            result = str(exc)

        if result is None:
            result = str()

        self.dispatch('on_output', result)
        self.dispatch('on_complete', result)


class ConsoleInput(TextInput):
    shell = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cursor_pos = 0
        # trick kivy, hehe ~ nekit
        self.prompt_pos = 0
        self.keyboard_on_key_down(None, (13, 'enter'), None, list())

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        code, key = keycode
        if (code not in (276, 273) and self.cursor_index() < self.prompt_pos) or \
                (code == 8 and self.cursor_index() == self.prompt_pos):
            self.cursor = self.get_cursor_from_index(self.prompt_pos)
            return
        if code == 13:
            self.validate_cursor_pos()
            text = self.text[self._cursor_pos:]

            if text.strip().startswith('clear'):
                self.text = ''
                self._cursor_pos = 0
                self.prompt()
                return

            elif text.strip():
                Clock.schedule_once(partial(self._run_cmd, text))

            else:
                Clock.schedule_once(self.prompt)
        elif code in [8, 127]:
            self.cancel_selection()
        elif code == 99 and modifiers == ['ctrl']:
            self.cancel_selection()
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def _run_cmd(self, cmd, *args):
        self.shell.run_command(str(cmd))

    def validate_cursor_pos(self, *args):
        if self.cursor_index() < self._cursor_pos:
            self.cursor = self.get_cursor_from_index(self._cursor_pos)

    def prompt(self, *args):
        ps = self.shell.term.format_ps()
        self._cursor_pos = self.cursor_index() + len(ps)
        self.prompt_pos = self._cursor_pos
        self.text += ps

    def on_output(self, output):
        if not self.text.endswith('\n'):
            self.text += '\n'
        self.text += output

        self.text += '\n'

    def on_complete(self, result):
        self.prompt()


class KivyConsole(BoxLayout, Shell):
    console_input = ObjectProperty(None)
    scroll_view = ObjectProperty(None)

    foreground_color = ListProperty((1, 0.5, 0, 1))
    background_color = ListProperty((0, 0, 0, 0.1))

    font_name = StringProperty(font)
    font_size = NumericProperty(14)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_output(self, output):
        self.console_input.on_output(output)

    def on_complete(self, output):
        self.console_input.on_complete(output)


class TermApp(App):
    def build(self):
        return KivyConsole()


if __name__ == '__main__':
    try:
        TermApp().run()
    except KeyboardInterrupt:
        exit()
