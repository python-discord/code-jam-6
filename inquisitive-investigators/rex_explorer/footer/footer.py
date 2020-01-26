from __future__ import annotations
from typing import Tuple, Union, Any

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObservableList
from kivy.core.window import Window, Keyboard

from .commands import *
from ..utils.paths import FOOTER_KV

Builder.load_file(FOOTER_KV)


class Footer(BoxLayout):
    """
    This is the bottom bar in our application.
    """

    def __init__(self, **kwargs: Any) -> None:
        super(Footer, self).__init__(**kwargs)
        self._open = False
        self.config_keyboard()

        # Keyboard binds
        self.actions = {
            '1': self.about,
            '2': self.edit,
            'q': self.photo_view,
            '3': self.copy,
            '4': self.down,
            '5': self.up,
            '6': self.mkdir,
            '7': self.create,
            '8': self.delete,
            '9': self.rename,
            '0': self.quit
        }

    def on_touch_up(self, touch):
        """
        Reregisters the keyboard.

        After selecting a text input,
        the keyboard becomes unregistered.

        This method will re-register the keyboard,
        so key presses will work again.
        """
        if self._keyboard is None:
            self.config_keyboard()

    def config_keyboard(self):
        """
        Re-registers the keyboard and
        rebinds on_key_down to our method.
        """
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _match(
            self, key: str, *args: Any, **kwargs: Any
    ) -> Union[bool, None]:
        """
        Calls the coresponding function to a specific key
        if it is defined within self.actions.
        """
        func = self.actions.get(key)
        return func(*args, **kwargs) if func else None

    def _on_keyboard_down(
            self,
            keyboard: Keyboard,
            keycode: Tuple[str, int],
            text: str,
            modifiers: ObservableList
    ) -> Union[bool, None]:
        """
        Ensures that multiple popups cannot be open
        at the same time.
        """
        if not self._open and self._match(keycode[1]):
            self._open = True

    def about(self) -> None:
        popup = AboutPopup(
            self, size_hint=(.7, .6),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True

    def edit(self) -> None:
        popup = EditPopup(
            self, size_hint=(.5, .3),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True

    def photo_view(self) -> None:
        popup = PhotoPopup(
            self, size_hint=(.5, .3),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True

    def copy(self):
        popup = CopyPopup(
            self, size_hint=(.5, .5),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True

    def mkdir(self) -> None:
        popup = Mkdir(
            self, size_hint=(.5, .5),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True

    def create(self) -> None:
        popup = CreatePopup(
            self, size_hint=(.5, .5),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True

    def down(self):
        RVL = self.parent.ids.left.ids.rv
        RVR = self.parent.ids.right.ids.rv
        if 1.0 >= RVL.scroll_y >= 0.1:
            RVL.scroll_y -= .1
        if 1.0 >= RVR.scroll_y >= 0.1:
            RVR.scroll_y -= .1

        return False

    def up(self):
        RVL = self.parent.ids.left.ids.rv
        RVR = self.parent.ids.right.ids.rv
        if 0.9 >= RVL.scroll_y >= 0.0:
            RVL.scroll_y += .1
        if 0.9 >= RVR.scroll_y >= 0.0:
            RVR.scroll_y += .1

        return False

    def rename(self) -> None:
        popup = RenamePopup(
            self, size_hint=(.5, .5),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True

    def delete(self) -> None:
        popup = DeletePopup(
            self, size_hint=(.7, .6),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True

    def quit(self) -> None:
        popup = QuitPopup(
            self, size_hint=(.5, .5),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )
        popup.open()
        return True
