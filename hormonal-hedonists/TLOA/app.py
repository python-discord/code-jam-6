from TLOA.core.constants import KEY_MAPPING
from TLOA.core.game import Game
from TLOA.core.view import GameView

from kivy.app import App
from kivy.core.window import Window


class HormonalHedonistsApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._game = Game()
        self._view = GameView(self._game)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        action = KEY_MAPPING.get(keycode[1])
        if action is None:
            return True

        return self._game.process_action(action)

    def build(self):
        return self._view
