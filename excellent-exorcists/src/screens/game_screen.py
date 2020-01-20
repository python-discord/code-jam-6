from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics import Color
from kivy.uix.label import Label
from kivy.core.window import Keyboard

from src.core.screen import Screen
from src.core.camera import OrthographicCamera


import random


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_x = 0
        self.player_y = 0

        self.zoom = 1
        self.fps = 0
        self.camera = OrthographicCamera(1280, 720)
        self.positions = [(random.randint(0, 1200), random.randint(0, 700)) for _ in range(100)]

    def on_resize(self, width: int, height: int):
        self.camera.set_size(width, height)

    def render(self, delta: float):
        self.set_projection_matrix(self.camera.get_projection())
        self.clear()

        Color(0, 0, 1)
        Rectangle(pos=(0, 0), size=(300, 300))

        Color(1., 1., 0)
        for pos in self.positions:
            Rectangle(pos=pos, size=(50, 50))

        Color(1, 0, 0)
        Rectangle(pos=(self.player_x, self.player_y), size=(20, 60))

        Color(0, 1, 0)
        Label(text=f'FPS: {self.fps}')

    def update(self, delta: float):
        self.camera.update(delta)
        self.camera.set_zoom(self.zoom)
        self.camera.set_position(self.player_x, self.player_y)

        player_speed = 50

        if Keyboard.keycodes['a'] in self.pressed_keys:
            self.player_x -= player_speed * delta
        elif Keyboard.keycodes['d'] in self.pressed_keys:
            self.player_x += player_speed * delta

        if Keyboard.keycodes['e'] in self.pressed_keys:
            self.zoom += delta
        elif Keyboard.keycodes['q'] in self.pressed_keys:
            self.zoom -= delta

        if Keyboard.keycodes['w'] in self.pressed_keys:
            self.player_y += player_speed * delta
        elif Keyboard.keycodes['s'] in self.pressed_keys:
            self.player_y -= player_speed * delta

        speed = 15
        self.fps = round(1 / delta)

        for i in range(len(self.positions)):
            x, y = self.positions[i]
            self.positions[i] = (x + speed * delta, y + speed * delta)
