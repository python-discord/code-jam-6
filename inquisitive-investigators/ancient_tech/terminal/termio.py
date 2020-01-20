import os
import sys
import shlex

from kivy.uix.textinput import TextInput
from kivy.properties import (
    Clock,
    partial,
    ObjectProperty
)


class TerminalInput(TextInput):
    """
    Sends terminal input and displays the output
    to and from the Shell.
    """

    shell = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(TerminalInput, self).__init__(*args, **kwargs)
        self._cursor_pos = 0
        self.init_terminal()

    def init_terminal(self, *args, **kwargs):
        """
        Get the current working directory 
        and username for the terminal.
        """
        self.current = os.getcwd()
        self.host = os.environ.get('COMPUTERNAME', 'kivy')
        self.user = os.environ.get('USER', '')

        if not self.user:
            self.user = os.environ.get('USERNAME', '')

        self.prompt()

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """
        Overrides _keyboard_on_key_down.
        """
        # Enter = 13
        # Execute command
        if keycode[0] == 13:
            self.validate_cursor_pos()
            text = self.text[self._cursor_pos:]

            if text.strip():
                Clock.schedule_once(partial(self._run_cmd, text))
            else:
                Clock.schedule_once(self.prompt)

        # Backspace = 8
        # Delete = 127
        elif keycode[0] in (8, 127):
            self.cancel_selection()

        # C = 99
        # Stop execution
        elif keycode[0] == 99 and modifiers == ['ctrl']:
            self.shell.stop()

        if self.cursor_index() < self._cursor_pos:
            return False

        return super(TerminalInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )

    def _run_cmd(self, cmd, *args, **kwargs):
        posix_ = True

        # Check OS
        if sys.platform[0] == 'w':
            posix_ = False

        cmds = shlex.split(str(cmd), posix=posix_)
        self.shell.run_cmd(cmds)

    def validate_cursor_pos(self, *args, **kwargs):
        if self.cursor_index() < self._cursor_pos:
            self.cursor = self.get_cursor_from_index(self._cursor_pos)


    def prompt(self, *args, **kwargs):
        at_info = f'[{self.user}@{self.host} {os.path.basename(str(self.current))}]>'

        self._cursor_pos = self.cursor_index() + len(at_info)
        self.text += at_info

    def on_output(self, output):
        self.text += output.decode()

    def on_complete(self, output):
        self.prompt()
