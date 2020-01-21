from typing import Any, Tuple

from kivy.uix.textinput import TextInput
from kivy.core.window import Keyboard
from kivy.properties import ObservableList

from ..utils.constants import KEYS


class EditorIO(TextInput):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(EditorIO, self).__init__(*args, **kwargs)

    def keyboard_on_key_down(
            self, 
            window: Keyboard, 
            keycode: Tuple[int, str], 
            text: str, 
            modifiers: ObservableList
        ):

        if keycode[0] in KEYS['x'] and 'ctrl' in modifiers:
            self.parent.parent.parent.manager.current = 'browser'

        elif keycode[0] in KEYS['del', 'backspace']:
            self.cancel_selection()

        return super(EditorIO, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )
