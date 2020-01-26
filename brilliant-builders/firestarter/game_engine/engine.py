from itertools import chain
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from firestarter.game_engine.resources_loader import load_resources
from firestarter.game_engine.sprite import Sprite
from firestarter.game_engine.utils import get_all_subclasses

from kivy.clock import Clock
from kivy.core.window import Keyboard, Window
from kivy.logger import Logger
from kivy.uix.widget import Widget

IMAGE_EXTENSIONS = ['png']


class Engine(Widget):
    resource_dir = (Path('.') / 'firestarter' / 'resources').absolute()
    X_PLAYER_OFFSET = -200  # how far from the center of the screen we want the player
    Y_PLAYER_OFFSET = -50  # how far from the center of the screen we want the player

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # bind the keyboard and its callbacks
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # keep track of the currently pressed keys in a set for smooth motion
        self.pressed_keys = set()

        # list of sprites
        self.sprites: List[Sprite] = []
        # list of elements that shouldn't be moved
        self.static_sprites: List[Sprite] = []
        # Object the camera should follow
        self.cam_target: Optional[Sprite] = None

        # dict of assets
        self.assets, self.levels = load_resources()

        self.sprite_classes = {cls.__name__: cls for cls in get_all_subclasses(Sprite)}

        # call the update method every frame
        Clock.schedule_interval(self._update, 1.0 / 60.0)
        Clock.schedule_interval(self._animate, 1.0 / 10.0)

    def move_camera(self, offset: Tuple[float, float]) -> None:
        for sprite in self.sprites:
            sprite.on_cam_move(offset)

    def add_player(self, sprite: Sprite) -> None:
        """Add the player sprite and set it as the cam target."""
        self.add_sprite(sprite)
        self.cam_target = sprite

    def add_sprite(self, sprite: Sprite, static: bool = False) -> None:
        """Add the sprite to the internal list and add the widget."""
        if static:
            self.static_sprites.append(sprite)
        else:
            self.sprites.append(sprite)

        self.add_widget(sprite)

    def add_sprites(self, sprites: List[Sprite], static: bool = False) -> None:
        """Add the list of sprites to the internal list and add the widgets."""
        if static:
            self.static_sprites.extend(sprites)
        else:
            self.sprites.extend(sprites)

        sprite: Sprite
        for sprite in sprites:
            self.add_widget(sprite)

    def update(self, dt: float) -> None:
        """This function will be overwritten by the user."""
        pass

    def unload_level(self, preserve: List = []) -> None:
        """Unload current level and kill all objects except objects in preserve."""
        Logger.info("Engine: Unloading current level")
        for sp in self.sprites:
            if sp not in preserve:
                sp.kill()

    def load_level(self, lv: Dict) -> dict:
        """Load level and return a dictionary of newly created objects."""
        Logger.info("Engine: Loading new level.")
        objs = {}
        obj_num = 0

        for obj in lv['object']:
            obj_id = obj['id'] if 'id' in obj else str(obj_num)

            Logger.debug(f"Engine: Creating object {obj_id} from class {obj['class']}")

            objs[obj_id] = (
                self.sprite_classes[obj['class']](
                    pos=obj['pos'],
                    engine=self,
                    **obj['args']
                )
            )
            obj_num += 1
        self.add_sprites(objs.values())
        return objs

    def _animate(self, dt: float) -> None:
        """Advance all the animations by one."""
        sprite: Sprite
        for sprite in chain(self.sprites, self.static_sprites):
            sprite.cycle_animation()

    def center_target(self) -> Tuple[float, float]:
        """Return a offset that will slowly center the target."""

        distance_to_center = ((self.cam_target.pos[0] - self.center_x - self.X_PLAYER_OFFSET),
                              (self.cam_target.pos[1] - self.center_y - self.Y_PLAYER_OFFSET))

        x_offset = -1 * distance_to_center[0] / (self.width / 2) * 5
        x_offset = x_offset * 2 if abs(x_offset) > .75 else 0

        y_offset = -1 * distance_to_center[1] / self.height * 5
        y_offset = y_offset if abs(y_offset) > .75 else 0

        return x_offset, y_offset

    def _update(self, dt: float) -> None:
        """Move the camera, update all sprites positions and call the users update function."""
        self.move_camera(self.center_target())
        sprite: Sprite
        for sprite in chain(self.sprites, self.static_sprites):
            if sprite.killed:
                self.sprites.remove(sprite)
                self.remove_widget(sprite)
            else:
                sprite.update(self.sprites)

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
