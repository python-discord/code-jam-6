from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image


class LedgerLayout(FloatLayout):
    child_widgets: list

    def __init__(self, *args, **kwargs):
        super(LedgerLayout, self).__init__()
        Window.bind(on_key_down=self._keydown)
        self.l_pos = ''
        self.m_pos = ''
        self.r_pos = ''

    def left(self, widget):
        widget.x = super().x

    def right(self, widget):
        widget.x = super().x + super().size[0] - 1.5 * widget.size[0]

    def top(self, widget):
        widget.y = super().y + super().size[1]-widget.size[1]

    def add_operator(self, widget):
        self.left(widget)
        self.top(widget)
        super().add_widget(widget)

    def add_left_digit(self, w):
        if self.l_pos == '':
            w.allow_stretch = True
            w.size_hint = (.3, .3)
            self.left(w)
            self.top(w)
            self.l_pos = w
            super().add_widget(w)

    def add_right_digit(self, w): 
        if self.r_pos == '':
            w.allow_stretch = True 
            w.size_hint = (.3, .3)
            self.right(w)
            self.top(w)
            self.r_pos = w
            super().add_widget(w)

    def _keydown(self, *args):
        print(args[1])
        if args[1] == 49:
            d = args[1] - 48
            l = Image(source=f'assets/graphics/cuneiform/c{d}.png')
            self.add_left_digit(l)
        if args[1] == 50:
            d = args[1] - 48
            l = Image(source=f'assets/graphics/cuneiform/c{d}.png')
            self.add_left_digit(l)

        if args[1] == 275:
            l = Image(source='assets/graphics/cuneiform/c1.png')
            self.add_left_digit(l)
            r = Image(source='assets/graphics/cuneiform/c1.png')
            self.add_right_digit(r)