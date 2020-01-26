from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
import math

A = 0


class LedgerLayout(FloatLayout):
    left_digit: bool
    middle_op: bool
    right_digit: bool
    side: str
    stored_right_digit: Widget
    stored_left_digit: Widget

    def __init__(self, *args, **kwargs):
        super(LedgerLayout, self).__init__()
        Window.bind(on_key_down=self._keydown)
        self.left_digit = False
        self.middle_op = False
        self.right_digit = False
        self.stored_right_digit = None
        self.stored_left_digit = None
        self.side = 'left'

    def toggle_side(self):
        if self.side == 'left':
            self.side = 'right'
        else:
            self.side = 'left'
            self.next_line()

    def left(self, widget: Widget):
        widget.x = self.x

    def right(self, widget: Widget):
        widget.x = self.x + self.size[0] - 1.5 * widget.size[0]

    def mid(self, widget: Widget):
        widget.x = self.x + self.size[0] / 2 - .6 * widget.size[0]

    def top(self, widget: Widget):
        widget.y = self.y + self.size[1] - widget.size[1]

    def add_operation(self, label: Label):
        if not self.middle_op:
            label.size_hint = (.3, .3)
            self.mid(label)
            self.top(label)
            self.mid_op = True
            self.add_widget(label)

    def add_next_digit(self, digit: BoxLayout):
        digit.allow_stretch = True
        digit.size_hint = (.3, .3)

        if not self.left_digit:
            self.left(digit)
            self.top(digit)
            self.left_digit = True
            self.add_widget(digit)
        elif not self.right_digit:
            self.right(digit)
            self.top(digit)
            self.right_digit = True
            self.add_widget(digit)
        else:
            return False

        return True

    def next_line(self):
        for child in self.children:
            child.y -= 0.8 * child.height

    def add_cuneiform(self, b10_number: int):
        # turn into an [b10, b10, b10], each at max 60
        if b10_number == 0:
            if self.side == 'left':
                self.left_digit = False
            else:
                self.right_digit = False

            self.add_next_digit(BoxLayout())
            return

        upper_limit = int(math.log(b10_number, 60)) + 1
        b60_number = []

        for i in range(upper_limit - 1, -1, -1):
            b60_number.append(b10_number // 60 ** i)
            b10_number %= 60 ** i

        layout = BoxLayout()

        for i in b60_number:
            ones = i % 10
            tens = (i // 10) * 10
            layout.add_widget(
                Image(source=f'assets/graphics/cuneiform/c{tens}.png')
            )

            layout.add_widget(
                Image(source=f'assets/graphics/cuneiform/c{ones}.png')
            )

        if self.side == 'left':
            self.left_digit = False
            if self.stored_left_digit:
                self.stored_left_digit.clear_widgets()
            self.stored_left_digit = layout
        else:
            self.right_digit = False
            if self.stored_right_digit:
                self.stored_right_digit.clear_widgets()
            self.stored_right_digit = layout

        self.add_next_digit(layout)

    def _keydown(self, _, keycode: int, __, key: str, *_args):
        global A

        if 48 <= keycode <= 57:
            A += keycode - 48
            self.add_cuneiform(A)

        # a numpad has to be used to not have to consider shift.
        elif key in ['/', '*', '-', '+']:
            self.add_operation(
                label=Label(
                    text=f'[color=000000]{key}[/color]',
                    markup=True,
                    font_size='58dp'
                )
            )

        elif keycode in [13, 271]:
            self.toggle_side()
