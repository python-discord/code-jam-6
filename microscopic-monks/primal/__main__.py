from kivy.app import App
from kivy.core.window import Window

from engine.engine import Engine
from engine.sprite import Sprite, Player


class MyGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player('testimg.png', [i / 2 for i in Window.size])

        self.add_sprite(self.player)

        for i in range(20):
            for j in range(20):
                thing = Sprite('testimg2.png', (100 * i, 100 * j))
                self.add_sprite(thing)

    def update(self, dt: float) -> None:
        self.player.pos = [i / 2 for i in Window.size]
        if 'w' in self.pressed_keys:
            for i in self.sprites:
                i.vel_y -= 3
        if 's' in self.pressed_keys:
            for i in self.sprites:
                i.vel_y += 3
        if 'a' in self.pressed_keys:
            for i in self.sprites:
                i.vel_x += 3
        if 'd' in self.pressed_keys:
            for i in self.sprites:
                i.vel_x -= 3


class Application(App):
    """Main application class."""

    def build(self) -> MyGame:
        """Return the root widget."""
        Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)
        Window.fullscreen = "auto"
        self.title = "Primal"
        game = MyGame()
        return game


if __name__ == "__main__":
    Application().run()