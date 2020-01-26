from kivy.uix.boxlayout import BoxLayout


class Ledger(BoxLayout):
    def __init__(self, **kwargs):
        super(Ledger, self).__init__(**kwargs)
        print('[ INIT LEDGER ]')

    def test(self):
        print(self.ids)
        self.display_rows.data = [
            {'data': ['TEST X', 'TEST Y', 'TEST OP', 'TEST Z']}
        ]

    def refresh(self):
        print(f"ids: {super(Ledger, self).ids}")
        # self.display_rows.data = [
        #     {'data': ['TEST X', 'TEST Y', 'TEST OP', 'TEST Z']}
        # ]

    def clear(self):
        self.rv.data = []

    # def add_cuneiform(self, b10_number: int):
    #     # turn into an [b10, b10, b10], each at max 60
    #     if b10_number == 0:
    #         if self.side == 'left':
    #             self.left_digit = False
    #         else:
    #             self.right_digit = False
    #
    #         self.add_next_digit(BoxLayout())
    #         return
    #
    #     upper_limit = int(math.log(b10_number, 60)) + 1
    #     b60_number = []
    #
    #     for i in range(upper_limit - 1, -1, -1):
    #         b60_number.append(b10_number // 60 ** i)
    #         b10_number %= 60 ** i
    #
    #     layout = BoxLayout()
    #
    #     for i in b60_number:
    #         ones = i % 10
    #         tens = (i // 10) * 10
    #         layout.add_widget(
    #             Image(source=f'assets/graphics/cuneiform/c{tens}.png')
    #         )
    #
    #         layout.add_widget(
    #             Image(source=f'assets/graphics/cuneiform/c{ones}.png')
    #         )
    #
    #     if self.side == 'left':
    #         self.left_digit = False
    #         if self.stored_left_digit:
    #             self.stored_left_digit.clear_widgets()
    #         self.stored_left_digit = layout
    #     else:
    #         self.right_digit = False
    #         if self.stored_right_digit:
    #             self.stored_right_digit.clear_widgets()
    #         self.stored_right_digit = layout
    #
    #     self.add_next_digit(layout)
