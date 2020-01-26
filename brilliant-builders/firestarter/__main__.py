import random
from typing import Any

from firestarter.game_engine.engine import Engine
from firestarter.game_engine.object import (
    FlameBuddy,
    GenericObject,
    Player,
    PlayerUiHeart,
)

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

from simpleaudio import PlayObject


class MyGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background
        self.background = GenericObject(self.assets['background'], (0, 0))
        self.add_sprite(self.background, static=True)

        # UI
        self.hearts = PlayerUiHeart(self.assets['hearts'], (0, self.height))
        self.hearts.change_mode(5)
        self.add_sprite(self.hearts, static=True)

        # FlameBuddy
        self.flameBuddy = FlameBuddy('flame', (40, 100), collide=False, engine=self, mode=0)

        # Player
        self.player = Player(self.assets['player'], (50, 90), death_sound=self.sounds['death'])
        self.player.bind(lives=self.update_hearts,
                         pos=lambda _, v: self.flameBuddy.on_player_pos(v))
        self.add_player(self.player)

        # Music
        self.musics = [self.sounds['music_01']]
        self.playing_music = self.play_music()

        self.add_sprite(self.flameBuddy)

        self.unload_level([self.player, self.hearts, self.flameBuddy])
        self.load_level(self.levels['level_01'])

    def update_hearts(self, _: Any, value: int) -> None:
        self.hearts.change_mode(value)
        if value <= 0:
            Clock.schedule_once(lambda *args: self.player.set_lives(5), .5)

    def on_height(self, _: Any, value: int) -> None:
        """Move the hearts to the top left corner."""
        self.hearts.pos = (0, value - 64)

    def play_music(self) -> PlayObject:
        return random.choice(self.musics).play()

    def update(self, dt: float) -> None:
        # Music update
        if not self.playing_music.is_playing():
            self.playing_music = self.play_music()

        # Player update
        if 'spacebar' in self.pressed_keys and self.player.is_standing:
            self.player.acc_y = 25
        if 'a' in self.pressed_keys:
            self.player.vel_x = -7

        if 'd' in self.pressed_keys:
            self.player.vel_x = 7

        if 'shift' in self.pressed_keys:
            self.player.wall_boost = True
        else:
            self.player.wall_boost = False


class Application(App):
    """Main application class."""

    def build(self) -> MyGame:
        """Return the root widget."""
        Window.clearcolor = (25 / 255, 51 / 255, 51 / 255, 1)
        self.title = 'FireStarter'
        game = MyGame()
        return game


if __name__ == "__main__":
    Application().run()
