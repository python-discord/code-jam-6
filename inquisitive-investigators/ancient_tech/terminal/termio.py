from __future__ import annotations
from typing import Any, Tuple, Union
import os
import sys
import shlex

from kivy.uix.textinput import TextInput
from kivy.core.window import Keyboard
from kivy.properties import (
    Clock,
    partial,
    ObjectProperty,
    ObservableList
)

from ..utils.constants import KEYS


class TerminalInput(TextInput):
    """
    Sends terminal input and displays the output
    to and from the Shell.
    """

    shell = ObjectProperty()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TerminalInput, self).__init__(*args, **kwargs)
        self._cursor_pos = 0
        self.init_terminal()

    def init_terminal(self) -> None:
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

    def keyboard_on_key_down(
            self,
            window: Keyboard,
            keycode: Tuple[int, str],
            text: str,
            modifiers: ObservableList
    ) -> Union[None, bool]:
        """
        Captures specific key presses
        and executes accordingly.
        """
        if keycode[0] in KEYS['enter']:
            self.validate_cursor_pos()
            text = self.text[self._cursor_pos - 1:]

            if text.strip():
                Clock.schedule_once(partial(self._run_cmd, text))
            else:
                Clock.schedule_once(self.prompt)

        elif keycode[0] in KEYS['del', 'backspace']:
            self.cancel_selection()

        elif keycode[0] in KEYS['c'] and 'ctrl' in modifiers:
            self.shell.stop()

        if self.cursor_index() < self._cursor_pos:
            return False

        return super(TerminalInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )

    def _run_cmd(
            self, cmd: str,
            *args: Any, **kwargs: Any
    ) -> None:
        """
        Checks OS for posix and
        executes commands.
        """
        posix_ = True

        # Check OS
        if sys.platform[0] == 'w':
            posix_ = False

        cmds = shlex.split(str(cmd), posix=posix_)
        self.shell.run_cmd(cmds)

    def validate_cursor_pos(
            self, *args: Any, **kwargs: Any
    ) -> None:
        if self.cursor_index() < self._cursor_pos:
            self.cursor = self.get_cursor_from_index(
                self._cursor_pos
            )

    def prompt(self, *args: Any, **kwargs: Any) -> None:
        """
        Prompts the user for an input.
        """
        at_info = (f'[{self.user}@{self.host} '
                   f'{os.path.basename(str(self.current))}]>'
                   )

        self._cursor_pos = self.cursor_index() + len(at_info) + 1
        self.text += at_info

    def on_cwd_change(self, cwd: str) -> None:
        """
        Updates the current working directory.
        """
        self.current = cwd

    def on_output(self, output: bytes) -> None:
        """
        Displays the output to terminal.
        """
        self.text += output.decode()

    def on_complete(self) -> None:
        """
        Prompts the user after a
        process has finished running.
        """
        self.prompt()
