from __future__ import annotations
from typing import Any, Tuple, Union

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObservableList
from kivy.core.window import Window, Keyboard

from .commands import *

Builder.load_file('./ancient_tech/footer/footer.kv')


class Footer(BoxLayout):

    def __init__(self, **kwargs: Any) -> None:
        super(Footer, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self) -> None:
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(
            self, 
            keyboard: Keyboard, 
            keycode: Tuple[str, int], 
            text: str, 
            modifiers: ObservableList
        ) -> Union[bool, None]:
        print(keycode)

        if keycode[1] == '1':
            self.about()
        if keycode[1] == '2':
            print('2')
        if keycode[1] == '3':
            print('3')
        if keycode[1] == '4':
            print('4')
        if keycode[1] == '5':
            print('5')
        if keycode[1] == '6':
            print('6')
        if keycode[1] == '7':
            print('7')
        if keycode[1] == '8':
            self.mkdir()
        if keycode[1] == '9':
            print('9')
        if keycode[1] == '0':
            self.quit()
        return True

    def about(self) -> None:
        popup = AboutPopup(size_hint=(.7, .6), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()

    def mkdir(self) -> None:
        popup = Mkdir(size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()

    def quit(self) -> None:
        popup = QuitPopup(size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
        popup.open()
