from typing import List, Tuple, Union

from firestarter.game_engine.engine import Engine
from firestarter.game_engine.sprite import Sprite, SpriteConfig

from kivy.properties import (
    NumericProperty, ReferenceListProperty)

from simpleaudio import WaveObject


class GenericObject(Sprite):
    def __init__(
            self,
            sprite: Union[SpriteConfig, str],
            pos: Tuple[int, int],
            collide: bool = False,
            mode: int = 1,
            engine: Engine = None,
            **kwargs
    ):
        # Resolve sprite if needed
        if isinstance(sprite, str):
            if not engine:
                raise ValueError('Argument engine required when searching for sprite')
            sprite = engine.assets[sprite]

        super().__init__(sprite, pos, **kwargs)

        self.collide = collide
        self.change_mode(mode)

    def on_collision(self, other: Sprite) -> bool:
        return self.collide


class PlayerUiHeart(Sprite):

    def on_collision(self, other: Sprite) -> bool:
        return False


class Platform(Sprite):
    def __init__(self, config: SpriteConfig, pos: Tuple[int, int] = (0, 0), **kwargs):
        super().__init__(config, pos, **kwargs)


class PickUpCoin(Sprite):
    def __init__(
            self,
            sprite: Union[SpriteConfig, str],
            pos: Tuple[int, int],
            collide: bool = False,
            mode: int = 1,
            engine: Engine = None,
            **kwargs
    ):
        # Resolve sprite if needed
        if isinstance(sprite, str):
            if not engine:
                raise ValueError('Argument engine required when searching for sprite')
            sprite = engine.assets[sprite]

        super().__init__(sprite, pos, **kwargs)

        self.activated = False
        self.collide = collide
        self.change_mode(mode)

    def on_collision(self, other: Sprite) -> bool:
        if isinstance(other, Player):
            print("coin +1!")
            other.score += 1
            self.kill()
        return self.collide


class FirePlaceCheckpoint(Sprite):
    def __init__(
            self,
            sprite: Union[SpriteConfig, str],
            pos: Tuple[int, int],
            collide: bool = False,
            mode: int = 1,
            engine: Engine = None,
            **kwargs
    ):
        # Resolve sprite if needed
        if isinstance(sprite, str):
            if not engine:
                raise ValueError('Argument engine required when searching for sprite')
            sprite = engine.assets[sprite]

        super().__init__(sprite, pos, **kwargs)

        self.activated = False
        self.collide = collide
        self.change_mode(mode)

    def on_animation_end(self) -> None:
        if self.activated:
            if self.current_mode == 2:
                self.change_mode(1)
            elif self.current_mode == 1:
                self.change_mode(0)

        self.current_frame = 0

    def update(self, other_sprites: List[Sprite]) -> None:
        pass

    def on_collision(self, other: Sprite) -> bool:
        if self.activated:
            return self.collide

        if isinstance(other, Player):
            self.activated = True
            print("Checkpoint set!")
            other.checkpoint = (self.pos[0], self.pos[1] + 70)

        return self.collide


class FlameBuddy(Sprite):

    acc_x = NumericProperty(0)
    acc_y = NumericProperty(0)
    acc = ReferenceListProperty(acc_x, acc_y)
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)

    def __init__(
            self,
            sprite: Union[SpriteConfig, str],
            pos: Tuple[int, int],
            collide: bool = False,
            mode: int = 1,
            engine: Engine = None,
            **kwargs
    ):
        # Resolve sprite if needed
        if isinstance(sprite, str):
            if not engine:
                raise ValueError('Argument engine required when searching for sprite')
            sprite = engine.assets[sprite]

        super().__init__(sprite, pos, **kwargs)

        self.activated = False
        self.collide = collide
        self.change_mode(mode)

    def on_player_pos(self, new_pos: Tuple[float, float]) -> None:
        distance_to_player = ((self.pos[0] - new_pos[0] + 10),
                              (self.pos[1] - new_pos[1] - 55))

        x_offset = -1 * distance_to_player[0] / 15

        y_offset = -1 * distance_to_player[1] / 15

        self.vel = (x_offset, y_offset)

    def update(self, other_sprites: List[Sprite]) -> None:
        self.vel = (self.vel_x + self.acc_x, self.vel_y + self.acc_y)
        # self.vel = (min(self.vel_x, 5), min(self.vel_y, 5))
        self.pos = (self.pos[0] + self.vel_x, self.pos[1] + self.vel_y)
        self.acc = (0, 0)

    def on_collision(self, other: Sprite) -> bool:
        return self.collide


class Player(Sprite):
    acc_x = NumericProperty(0)
    acc_y = NumericProperty(0)
    acc = ReferenceListProperty(acc_x, acc_y)
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)

    score = NumericProperty(0)
    lives = NumericProperty(5)

    def __init__(
            self,
            config: SpriteConfig,
            pos: Tuple[int, int] = (0, 0),
            death_sound: WaveObject = None,
            **kwargs
    ) -> None:
        super().__init__(config, pos, **kwargs)
        self.is_standing: bool = False
        self.checkpoint: Tuple[int, int] = pos
        self.respawn: Tuple[int, int] = pos

        self.death_sound = death_sound

    def set_lives(self, value: int) -> None:
        """Set the players lives."""
        self.lives = value

    def on_cam_move(self, offset: Tuple[float, float]) -> None:
        super().on_cam_move(offset)
        self.respawn = (self.respawn[0] + offset[0], self.respawn[1] + offset[1])
        self.checkpoint = (self.checkpoint[0] + offset[0], self.checkpoint[1] + offset[1])

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

        if self.pos[1] < 0:
            # we fell out of the map!
            self.lives -= 1
            if self.death_sound:
                self.death_sound.play()
            if self.lives > 0:
                # respawn at the checkpoint
                self.pos = self.checkpoint
            else:
                self.pos = self.respawn

    def collides_with(self, other_sprites: List[Sprite]) -> bool:
        # deal with collisions
        for sprite in other_sprites:
            if sprite != self and self.collide_widget(sprite):
                if sprite.on_collision(self):
                    return True
