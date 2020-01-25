from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label


class LedgerLayout(FloatLayout):
    left_digit: bool
    middle_op: bool
    right_digit: bool

    def __init__(self, *args, **kwargs):
        super(LedgerLayout, self).__init__()
        Window.bind(on_key_down=self._keydown)
        self.left_digit = False
        self.middle_op = False
        self.right_digit = False

    def left(self, widget: Widget):
        widget.x = self.x

    def right(self, widget: Widget):
        widget.x = self.x + self.size[0] - 1.5 * widget.size[0]

    def mid(self, widget: Widget):
        widget.x = self.x + self.size[0] / 2 - .6 * widget.size[0]

    def top(self, widget: Widget):
        widget.y = self.y + self.size[1]-widget.size[1]

    def add_operation(self, label: Label):
        if not self.middle_op:
            label.size_hint = (.3, .3)
            self.mid(label)
            self.top(label)
            self.mid_op = True
            self.add_widget(label)

    def add_next_digit(self, image: Image):
        image.allow_stretch = True
        image.size_hint = (.3, .3)

        if not self.left_digit:
            self.left(image)
            self.top(image)
            self.left_digit = True
            self.add_widget(image)
        elif not self.right_digit:
            self.right(image)
            self.top(image)
            self.right_digit = True
            self.add_widget(image)
        else:
            return False

        return True

    def next_line(self):
        for child in self.children:
            child.y -= 0.8 * child.height

    def _keydown(self, _, keycode: int, __, key: str, *_args):
        if 48 <= keycode <= 57:
            self.add_next_digit(
                image=Image(source=f'assets/graphics/cuneiform/c{key}.png')
            )

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
            self.left_digit = False
            self.middle_op = False
            self.right_digit = False
            self.next_line()
