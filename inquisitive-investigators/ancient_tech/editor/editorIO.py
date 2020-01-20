from typing import Any, Tuple

from kivy.uix.textinput import TextInput
from kivy.core.window import Keyboard
from kivy.properties import ObservableList


class EditorIO(TextInput):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(EditorIO, self).__init__(*args, **kwargs)
        self._cursor_pos = 0

    def keyboard_on_key_down(
            self, 
            window: Keyboard, 
            keycode: Tuple[int, str], 
            text: str, 
            modifiers: ObservableList
        ):

        pass
    