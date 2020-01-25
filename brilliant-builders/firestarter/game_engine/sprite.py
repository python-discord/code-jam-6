from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget


@dataclass
class SpriteConfig:
    file_path: Path
    texture: Texture
    size: List[int, int] = (64, 64)
    animation_modes: int = 1
    frame_count: List[int, ...] = (1,)
    size_hint: List[int, int] = (64, 64)


class Sprite(Widget):
    resource_dir = (Path('.') / 'firestarter' / 'resources').absolute()

    def __init__(self, config: SpriteConfig, pos: Tuple[int, int] = (0, 0), **kwargs) -> None:
        super().__init__(**kwargs)

        self.killed: bool = False
        self.size = config.size
        self.pos = pos
        self.config = config
        self.current_mode = 0
        self.current_frame = 0

        with self.canvas:
            self.bg_rect = Rectangle(texture=self.config.texture.get_region(0, 0, *config.size),
                                     pos=self.pos,
                                     size=self.size)
            self.bg_rect.texture.mag_filter = 'nearest'
        self.bind(pos=self.redraw)

    def cycle_animation(self) -> None:
        """Cycle the animation by one frame forwards."""
        self.current_frame += 1
        # if we exceed the frames of animation for this mode, go back to the beginning
        self.current_frame = self.current_frame % self.config.frame_count[self.current_mode]
        # calculate the new texture region
        new_pos = (
            self.current_frame * self.config.size[0],
            self.current_mode * self.config.size[1]
        )
        # set the texture
        self.bg_rect.texture = self.config.texture.get_region(*new_pos, *self.config.size)

    def change_mode(self, mode: int) -> None:
        """Change the mode of animation."""
        # if we exceed the number of modes, go back to the beginning
        mode = mode % self.config.animation_modes
        self.current_mode = mode

    def redraw(self, *args) -> None:
        """Redraw the rectangle after moving the sprite."""
        self.bg_rect.pos = self.pos

    def update(self, *args) -> None:
        raise NotImplementedError()

    def on_collision(self, other: Sprite) -> bool:
        """Return False if you can pass through, else return True"""
        return True

    def kill(self) -> None:
        self.killed = True
