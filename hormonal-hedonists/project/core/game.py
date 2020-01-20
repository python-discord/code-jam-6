from project.core.constants import Actions, KEY_MAPPING

from kivy.core.window import Window
from kivy.uix.widget import Widget


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        action = KEY_MAPPING.get(keycode[1])
        if action is None:
            return

        if action == Actions.MOVE_LEFT:
            print('Moving Left')
        if action == Actions.MOVE_RIGHT:
            print('Moving Right')
        if action == Actions.MOVE_UP:
            print('Moving Up')
        if action == Actions.MOVE_DOWN:
            print('Moving Down')
        if action == Actions.JUMP:
            print('Jumping')
        return True
