from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label


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

    def mid(self, widget):
        widget.x = super().x + super().size[0] / 2 - .6 * widget.size[0]

    def top(self, widget):
        widget.y = super().y + super().size[1]-widget.size[1]

    def add_operator(self, widget):
        self.left(widget)
        self.top(widget)
        super().add_widget(widget)

    def add_middle(self, w):
        if self.m_pos == '':
            w.allow_stretch = True
            w.size_hint = (.3, .3)
            self.mid(w)
            self.top(w)
            self.m_pos = w
            super().add_widget(w)

    def add_left_digit(self, w):
        if self.l_pos == '':
            w.allow_stretch = True
            w.size_hint = (.3, .3)
            self.left(w)
            self.top(w)
            self.l_pos = w
            super().add_widget(w)
            return True
        return False

    def add_right_digit(self, w): 
        if self.r_pos == '':
            w.allow_stretch = True 
            w.size_hint = (.3, .3)
            self.right(w)
            self.top(w)
            self.r_pos = w
            super().add_widget(w)
            return True
        return False

    def next_line(self):
        for child in super(LedgerLayout, self).children:
            child.y -= child.size[1] - .2 * child.size[1]

    def _keydown(self, *args):
        print(args[1])
        if(args[1] >= 257 and args[1] <= 265):
            if not self.add_left_digit(Image(source=f'assets/graphics/cuneiform/c{args[1] - 256}.png')):
                self.add_right_digit(Image(source=f'assets/graphics/cuneiform/c{args[1] - 256}.png'))
        if(args[1] == 267):
            l = Label(text="[color=000000]/[/color]", markup=True)
            l.font_size = '58dp'
            l.color = 0, 0, 0, 0
            self.add_middle(l)
        if(args[1] == 268):
            l = Label(text="[color=000000]*[/color]", markup=True)
            l.font_size = '58dp'
            l.color = 0, 0, 0, 0
            self.add_middle(l)
        if(args[1] == 269):
            l = Label(text="[color=000000]-[/color]", markup=True)
            l.font_size = '58dp'
            l.color = 0, 0, 0, 0
            self.add_middle(l)
        if(args[1] == 270):
            l = Label(text="[color=000000]+[/color]", markup=True)
            l.font_size = '58dp'
            l.color = 0, 0, 0, 0
            self.add_middle(l)
        if(args[1] == 271):
            self.l_pos = ''
            self.m_pos = ''
            self.r_pos = ''
            self.next_line()