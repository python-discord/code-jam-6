from kivy.app import App
from kivy.core.window import Window

from engine.engine import Engine
from engine.sprite import Sprite, Player
from engine.perlin import perlin_array


class MyGame(Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player('testimg.png', [i / 2 for i in Window.size])
        self.map = perlin_array()

        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                m = i - 15
                n = j - 15
                v = (m**2 + n**2)**0.5
                a = self.map[i][j] - 0.9 ** (22 - v) + 0.05
                if a > 0.75:
                    thing = Sprite('i.png', (1000 * m, 1000 * n), (1000, 1000))
                    self.add_sprite(thing)
                elif a > 0.5:
                    thing = Sprite('l.png', (1000 * m, 1000 * n), (1000, 1000))
                    self.add_sprite(thing)
                elif a > 0.25:
                    thing = Sprite('s.png', (1000 * m, 1000 * n), (1000, 1000))
                    self.add_sprite(thing)
                else:
                    thing = Sprite('w.png', (1000 * m, 1000 * n), (1000, 1000))
                    self.add_sprite(thing)
        self.add_sprite(self.player)

    def update(self, dt: float) -> None:
        self.player.pos = [i / 2 for i in Window.size]
        if 'w' in self.pressed_keys:
            for i in self.sprites:
                i.vel_y -= 5
        if 's' in self.pressed_keys:
            for i in self.sprites:
                i.vel_y += 5
        if 'a' in self.pressed_keys:
            for i in self.sprites:
                i.vel_x += 5
        if 'd' in self.pressed_keys:
            for i in self.sprites:
                i.vel_x -= 5


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