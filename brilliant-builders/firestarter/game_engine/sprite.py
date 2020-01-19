from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.properties import (
    NumericProperty, ReferenceListProperty)
from kivy.uix.widget import Widget


@dataclass
class SpriteConfig:
    file_path: Path
    texture: Texture
    size: Tuple[int, int] = (64, 64)
    animation_modes: int = 1
    frame_count: Tuple[int, ...] = (1,)
    size_hint: Tuple[int, int] = (64, 64)


class Sprite(Widget):
    resource_dir = (Path('.') / 'resources').absolute()

    def __init__(self, config: SpriteConfig, pos: Tuple[int] = (0, 0), **kwargs) -> None:
        super().__init__(**kwargs)

        self.size = (50, 50)
        self.pos = pos
        self.config = config
        self.current_mode = 0
        self.current_frame = 0

        with self.canvas:
            self.bg_rect = Rectangle(texture=self.config.texture.get_region(0, 0, *config.size),
                                     pos=self.pos,
                                     size=self.size)
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

    def update(self) -> None:
        raise NotImplementedError()


class Player(Sprite):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)

    def __init__(self, config: SpriteConfig, pos: tuple = (0, 0), **kwargs) -> None:
        super().__init__(config, pos, **kwargs)

    def update(self) -> None:
        # update the position
        self.pos = (self.pos[0] + self.vel_x, self.pos[1] + self.vel_y)
        # dampen the velocity to come to a stop
        self.vel_x *= .5
        self.vel_y *= .5
        # apply some downwards velocity
        self.vel_y -= 2
        # make sure we don't fall out of the world
        if self.pos[1] < 50:
            self.pos = (self.pos[0], 50)
