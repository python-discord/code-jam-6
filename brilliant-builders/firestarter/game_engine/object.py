from typing import List, Tuple, Union

from firestarter.game_engine.engine import Engine
from firestarter.game_engine.sprite import Sprite, SpriteConfig

from kivy.properties import (
    NumericProperty, ReferenceListProperty)


class GenericSprite(Sprite):
    def __init__(
            self,
            config: Union[SpriteConfig, str],
            pos: Tuple[int, int],
            collide: bool = False,
            mode: int = 1,
            engine: Engine = None,
            **kwargs
    ):
        # Resolve config if needed
        if isinstance(config, str):
            if not engine:
                raise ValueError('Argument engine required when searching for sprite')
            config = engine.assets[config]

        super().__init__(config, pos, **kwargs)

        self.collide = collide
        self.change_mode(mode)

    def update(self, *args) -> None:
        pass

    def on_collision(self, other: Sprite) -> bool:
        return self.collide


class Platform(Sprite):
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
