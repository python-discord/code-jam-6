from typing import Any, Tuple

from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.core.window import Keyboard
from kivy.properties import (
    StringProperty,    
    ObservableList
)

from .save import SavePopup
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
        """
        Captures specific key presses
        and executes accordingly.
        """
        if keycode[0] in KEYS['s'] and 'ctrl' in modifiers:
            popup = SavePopup(
                self, size_hint=(.5, .5), 
                pos_hint={
                    'center_x': .5, 'center_y': .5
                }
            )
            popup.open()

        elif keycode[0] in KEYS['enter']:
            self.focus = True
            text = list(self.text)
            text.insert(self.cursor_index(), '\n')
            self.text = ''.join(text)
            Clock.schedule_once(self._focus)
            
        elif keycode[0] in KEYS['esc']:
            self.root.manager.current = 'browser'

        elif keycode[0] in KEYS['del', 'backspace']:
            self.cancel_selection()

        return super(EditorIO, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )

    def _focus(self, event) -> None:
        """
        Refocus mouse cursor into TextInput.
        """
        self.focus = True
