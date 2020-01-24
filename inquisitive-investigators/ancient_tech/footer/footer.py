from __future__ import annotations
from typing import Any, Tuple, Union

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObservableList
from kivy.core.window import Window, Keyboard
from kivy.uix.textinput import TextInput

from .commands import *

Builder.load_file('./ancient_tech/footer/footer.kv')


class Footer(BoxLayout):

    def __init__(self, **kwargs: Any) -> None:
        super(Footer, self).__init__(**kwargs)
        self._open = False
        self.config_keyboard()
        self.actions = {
            '1': self.about,
            '2': self.view,
            '4': self.down,
            '5': self.up,
            '6': self.mkdir,
            '7': self.delete,
            '8': self.create,
            '9': self.quit
        }

    def on_touch_up(self, touch):
        if self._keyboard is None:
            self.config_keyboard()

    def config_keyboard(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _match(
            self, key: str, *args: Any, **kwargs: Any
    ) -> Union[bool, None]:
        func = self.actions.get(key)
        return func(*args, **kwargs) if func else None

    def _on_keyboard_down(
            self,
            keyboard: Keyboard,
            keycode: Tuple[str, int],
            text: str,
            modifiers: ObservableList
    ) -> Union[bool, None]:
        if not self._open and self._match(keycode[1]):
            self._open = True

    def about(self) -> None:
        popup = AboutPopup(self, size_hint=(.7, .6), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()
        return True

    def mkdir(self) -> None:
        popup = Mkdir(self, size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()
        return True

    def create(self) -> None:
        popup = CreatePopup(self, size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()
        return True

    def view(self) -> None:
        # not working
        self.parent.manager.current = 'text_editor'
        return True

    def down(self):
        RVL = self.parent.ids.left.ids.rv
        RVR = self.parent.ids.right.ids.rv
        if 1.0 >= RVL.scroll_y >= 0.1:
            RVL.scroll_y -= .1
        if 1.0 >= RVR.scroll_y >= 0.1:
            RVR.scroll_y -= .1

    def up(self):
        RVL = self.parent.ids.left.ids.rv
        RVR = self.parent.ids.right.ids.rv
        if 0.9 >= RVL.scroll_y >= 0.0:
            RVL.scroll_y += .1
        if 0.9 >= RVR.scroll_y >= 0.0:
            RVR.scroll_y += .1

    def delete(self) -> None:
        popup = DeletePopup(self, size_hint=(.7, .6), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()
        return True

    def quit(self) -> None:
        popup = QuitPopup(self, size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()
        return True
