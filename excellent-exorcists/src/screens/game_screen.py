from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics import Color
from kivy.uix.label import Label
from src.core.screen import Screen

import random


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fps = 0
        self.positions = [(random.randint(0, 600), random.randint(0, 300)) for _ in range(100)]

    def on_resize(self, width: int, height: int):
        pass

    def render(self, delta: float):
        self.clear()
        Color(1., 1., 0)

        for pos in self.positions:
            Rectangle(pos=pos, size=(50, 50))

        Color(0, 1, 0)
        Label(text=f'FPS: {self.fps}')

    def update(self, delta: float):
        speed = 10
        self.fps = round(1 / delta)

        for i in range(len(self.positions)):
            x, y = self.positions[i]
            self.positions[i] = (x + speed * delta, y + speed * delta)
