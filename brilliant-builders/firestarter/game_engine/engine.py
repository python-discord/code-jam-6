import os
from pathlib import Path
from typing import List


from firestarter.game_engine.sprite import Sprite, SpriteConfig

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.window import Keyboard, Window
from kivy.uix.widget import Widget

import toml

IMAGE_EXTENSIONS = ['png']


class Engine(Widget):
    resource_dir = (Path('.') / 'firestarter' / 'resources').absolute()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # bind the keyboard and its callbacks
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # keep track of the currently pressed keys in a set for smooth motion
        self.pressed_keys = set()

        # list of sprites
        self.sprites: List[Sprite] = []  # TODO: make this only accept sprite classes

        # dict of assets
        self.assets = self.load_sprite_sheets()

        # call the update method every frame
        Clock.schedule_interval(self._update, 1.0 / 60.0)
        Clock.schedule_interval(self._animate, 1.0 / 10.0)

    def load_sprite_sheets(self) -> dict:
        """Load all images in the resources/sprites directory to the gpu"""
        assets = {}
        for sprite_sheet in [
            sp for sp in os.listdir(self.resource_dir / 'sprites')
            if sp.rsplit('.', 1)[-1] in IMAGE_EXTENSIONS
        ]:
            img_path = (self.resource_dir / 'sprites' / sprite_sheet).as_posix()
            texture = CoreImage(img_path).texture
            texture.mag_filter = 'nearest'

            config_file = (
                self.resource_dir / 'sprites' / (sprite_sheet.rsplit('.', 1)[0] + '_config.toml')
            ).as_posix()
            with open(config_file) as f:
                config_dict = toml.load(f)['animation']

            config = SpriteConfig(
                self.resource_dir / 'sprites' / sprite_sheet,
                texture,
                config_dict['size'],
                config_dict['modes'],
                config_dict['frame_count']
            )
            assets[sprite_sheet.rsplit('.', 1)[0]] = config
        return assets

    def add_sprite(self, sprite: Sprite) -> None:
        """Add the sprite to the internal list and add the widget."""
        self.sprites.append(sprite)
        self.add_widget(sprite)

    def update(self, dt: float) -> None:
        """This function will be overwritten by the user."""
        pass

    def _animate(self, dt: float) -> None:
        """Advance all the animations by one."""
        sprite: Sprite
        for sprite in self.sprites:
            sprite.cycle_animation()

    def _update(self, dt: float) -> None:
        """Update all sprites positions and call the users update function."""
        sprite: Sprite
        for sprite in self.sprites:
            sprite.update()

        self.update(dt)

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
        self.pressed_keys.add(key_code[1])

    def _on_keyboard_up(self, keyboard: Keyboard, key_code: tuple) -> None:
        """
        Remove the pressed key to the set of pressed keys.

        :param keyboard: keyboard instance
        :param key_code: pressed key code
        :return: None
        """
        self.pressed_keys.remove(key_code[1])
