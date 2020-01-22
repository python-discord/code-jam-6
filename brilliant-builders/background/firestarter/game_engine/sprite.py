from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

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


class Platform(Sprite):
    def __init__(self, config: SpriteConfig, pos: Tuple[int, int] = (0, 0), **kwargs):
        super().__init__(config, pos, **kwargs)

    def update(self, other_sprites: List[Sprite]) -> None:
        pass


class Duck(Sprite):
    def __init__(self, config: SpriteConfig, pos: Tuple[int, int] = (0, 0), **kwargs):
        super().__init__(config, pos, **kwargs)

    def update(self, other_sprites: List[Sprite]) -> None:
        pass


class PickUpCoin(Sprite):
    def __init__(self, config: SpriteConfig, pos: Tuple[int, int] = (0, 0), **kwargs):
        super().__init__(config, pos, **kwargs)

    def update(self, other_sprites: List[Sprite]) -> None:
        pass

    def on_collision(self, other: Sprite) -> bool:
        if isinstance(other, Player):
            print("coin +1!")
            other.score += 1
            self.kill()
        return False


class Player(Sprite):
    acc_x = NumericProperty(0)
    acc_y = NumericProperty(0)
    acc = ReferenceListProperty(acc_x, acc_y)
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)

    def __init__(self, config: SpriteConfig, pos: Tuple[int, int] = (0, 0), **kwargs) -> None:
        super().__init__(config, pos, **kwargs)
        self.is_standing: bool = False
        self.score: int = 0

    def update(self, other_sprites: List[Sprite]) -> None:
        """Update the players position and handle collisions (very inefficiently!!)"""
        # update the position
        old_pos = (self.pos[0], self.pos[1])

        # update our velocity
        self.vel = (self.vel_x + self.acc_x, self.vel_y + self.acc_y)

        # first try to apply up/downwards velocity
        self.pos = (self.pos[0] + self.vel_x, self.pos[1] + self.vel_y)
        if self.collides_with(other_sprites):  # we are colliding in x or y

            self.pos = (old_pos[0], old_pos[1])
            self.pos = (self.pos[0] + self.vel_x, self.pos[1])

            if self.collides_with(other_sprites):  # colliding in x
                self.vel_x = 0
                self.pos = (old_pos[0], old_pos[1])

            old_pos = (self.pos[0], self.pos[1])
            self.pos = (old_pos[0], old_pos[1] + self.vel_y)

            if self.collides_with(other_sprites):  # colliding in y
                self.vel_y = 0
                self.pos = (old_pos[0], old_pos[1])
                # this also tells us we are standing on something!
                self.is_standing = True
        else:
            self.is_standing = False

        # dampen the velocity to come to a stop
        if self.is_standing:
            self.vel_x *= .5
            self.vel_y *= .5
        else:
            self.vel_x *= .75
            self.vel_y *= .90
        # apply some downwards acceleration (gravity)
        self.acc_y = -1

    def collides_with(self, other_sprites: List[Sprite]) -> bool:
        # deal with collisions
        for sprite in other_sprites:
            if sprite != self and self.collide_widget(sprite):
                if sprite.on_collision(self):
                    return True

    def on_collision(self, other: Sprite) -> None:
        pass
