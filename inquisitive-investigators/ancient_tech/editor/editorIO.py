from typing import Any, Tuple

from kivy.uix.textinput import TextInput
from kivy.core.window import Keyboard
from kivy.properties import (
    StringProperty,    
    ObservableList
)

from ..utils.constants import KEYS


class EditorIO(TextInput):
    file_path = StringProperty()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(EditorIO, self).__init__(*args, **kwargs)

    def keyboard_on_key_down(
            self, 
            window: Keyboard, 
            keycode: Tuple[int, str], 
            text: str, 
            modifiers: ObservableList
        ):

        if keycode[0] in KEYS['s'] and 'ctrl' in modifiers:
            pass

        elif keycode[0] in KEYS['esc']:
            self.parent.parent.parent.manager.current = 'browser'

        elif keycode[0] in KEYS['del', 'backspace']:
            self.cancel_selection()

        return super(EditorIO, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )
