from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.recycleview import RecycleView

import math
from random import sample
from string import ascii_lowercase


class Ledger(BoxLayout):
    def __init__(self, **kwargs):
        super(Ledger, self).__init__(**kwargs)
        self.rv = RecycleView()

    def test(self):
        self.rv.data = [{'test_x': ''.join(sample(ascii_lowercase, 6))}
                        for x in range(10)]

    def refresh(self, rows):
        for row in rows:
            print(f"Refreshing row: {row}")
            self.rv.data = [
                {'test_x': row[0]},
                {'test_y': row[1]},
                {'test_op': row[2]},
                {'test_z': row[3]}
            ]

    def clear(self):
        self.rv.data = []

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
