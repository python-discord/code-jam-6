from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.base import runTouchApp


class Scrolling(Widget):
    def __init__(self, **kwargs):
        super(Scrolling, self).__init__(**kwargs)
        Clock.schedule_once(self.texture_init, 0)
        Clock.schedule_interval(self.update, 1. / 60)

    def texture_init(self, dt):
        self.canvas.children[-1].texture.wrap = 'repeat'

    def update(self, dt):
        for i in range(0, 8, 2):
            self.tex_coords[i] += dt / 3.


root = Builder.load_string('''
Scrolling:

<Scrolling>:
    tex_coords: [0, 0, 0, 1, 1, 1, 1, 0]
    canvas:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'ui\img\morse_code_bg.jpg'
            tex_coords: root.tex_coords
''')



runTouchApp(root)
