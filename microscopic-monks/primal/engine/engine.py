from typing import List

from kivy.clock import Clock
from kivy.core.window import Keyboard, Window
from kivy.uix.widget import Widget

from .screen import Screen


class Engine(Widget):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # bind the keyboard and its callbacks
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        Window.bind(mouse_pos=self.update_mouse_pos)

        # keep track of the currently pressed keys in a set for smooth motion
        self.pressed_keys = set()

        # keep track of the current mouse position
        self.mouse_position = 0, 0

        # list of screens to update
        self.screens: List[Screen] = []  # TODO: make this only accept screen classes

        # call the update method every frame
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update_mouse_pos(self, _, n):
        self.mouse_position = n

    def add_screen(self, screen: Screen) -> None:
        """Add the sprite to the internal list and add the widget."""
        if screen not in self.screens:
            screen.set_engine(self)

            self.screens.append(screen)
            self.add_widget(screen)

    def update(self, dt: float) -> None:
        """Call update and render on each screen """
        for screen in self.screens:
            screen.update(dt)

    def _keyboard_closed(self) -> None:
        """Clean up once the keyboard is closed."""
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self,
                          keyboard: Keyboard,
                          key_code: tuple,
                          text: str,
                          modifiers: List) -> None:
        """
        Add the pressed key to the set of pressed keys.
        :param keyboard: keyboard instance
        :param key_code: pressed key code
        :param text: key as text
        :param modifiers: modifiers pressed
        :return: None
        """
        self.pressed_keys.add(key_code[0])

    def _on_keyboard_up(self, keyboard: Keyboard, key_code: tuple) -> None:
        """
        Remove the pressed key to the set of pressed keys.
        :param keyboard: keyboard instance
        :param key_code: pressed key code
        :return: None
        """
        self.pressed_keys.discard(key_code[0])
