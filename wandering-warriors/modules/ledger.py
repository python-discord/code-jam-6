from kivy.uix.boxlayout import BoxLayout
import pandas as pd


class Ledger(BoxLayout):
    def __init__(self, **kwargs):
        super(Ledger, self).__init__(**kwargs)
        print('[ INIT LEDGER ]')
        self.df = pd.DataFrame(columns=['x', 'y', 'op', 'z'])
        self.col = 'x'
        self.row = 1
        self.new_row()

    def select(self, col: str):
        """select column: ['x', 'y', 'z']"""
        if col not in ['x', 'y', 'z']:
            print(f"WARNING: Invalid column: {col}")
            pass
        else:
            self.col = col

    def update(self, n: int, op: str = '='):
        """update active cell"""
        if op == '+':
            self.df.at[self.row, self.col] += n
        if op == '-':
            self.df.at[self.row, self.col] -= n
        if op == '*':
            self.df.at[self.row, self.col] *= n
        if op == '/':
            self.df.at[self.row, self.col] /= n
        if op == '=':
            self.df.at[self.row, self.col] = n
        print(self.df)
        self.update_ledger()

    def new_row(self):
        """add and select new row at bottom of ledger"""
        index = len(self.df.index) + 1
        self.df.loc[index] = {'x': 0, 'y': 0, 'op': None, 'z': 0}
        self.row = index
        self.col = 'x'
        print(self.df)

    def update_ledger(self):
        """update ledger view with current data"""
        rows = self.df.values.astype('str')
        print(f"ROWS: {rows}")
        print(f"ids: {self.ids}")
        self.rv.data = [
            {'value': row} for row in rows
        ]

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
