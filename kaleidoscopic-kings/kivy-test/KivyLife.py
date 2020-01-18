from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty

import random
from kivy.clock import Clock


class Life:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_state = [[random.randint(1, 10) > 8 for _ in range(width)] for _ in range(height)]
        self.has_been_alive = [i[:] for i in self.current_state]

    def update(self):
        new_state = [sl[:] for sl in self.current_state]
        for i in range(self.width):
            for j in range(self.height):
                neighbours = 0
                for l in range(-1, 2):
                    for r in range(-1, 2):
                        x, y = i + l, j + r
                        if not (l == 0 and r == 0) and x < self.width and y < self.height and x > 0 and y > 0:
                            neighbours += self.current_state[x][y]
                if neighbours < 2:
                    new_state[i][j] = False
                if neighbours == 3:
                    new_state[i][j] = True
                    self.has_been_alive[i][j] = True
                if neighbours > 3:
                    new_state[i][j] = False

        self.current_state = new_state


class Cell(Widget):
    r, g, b, a = NumericProperty(1), NumericProperty(0), NumericProperty(0), NumericProperty(0)


class PongGame(Widget):
    w, h = 100, 100
    life = Life(w, h)
    cells = []

    def start(self):
        for i in range(self.w):
            r = []
            self.cells.append(r)
            for j in range(self.h):
                w = Cell(pos=(i * 5, j * 5))
                self.add_widget(w)
                r.append(w)

    def on_touch_up(self, t):
        x, y = int(t.x) // 5, int(t.y) // 5

        self.cells[x][y].r = 1
        self.life.current_state[x][y] = 1

    def render(self, _):
        self.life.update()
        for i in range(self.w):
            for j in range(self.h):
                if self.life.current_state[i][j]:
                    self.cells[i][j].r = 1
                else:
                    if self.life.has_been_alive[i][j]:
                        self.cells[i][j].r = 0.1
                    else:
                        self.cells[i][j].r = 0


class LifeApp(App):
    def build(self):
        game = PongGame()
        game.start()
        Clock.schedule_interval(game.render, 1.1 / 60.0)
        return game


if __name__ == '__main__':
    LifeApp().run()

