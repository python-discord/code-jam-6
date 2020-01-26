from kivy.uix.boxlayout import BoxLayout
import pandas as pd


class Ledger(BoxLayout):
    """
    Ledger data structure:
    x: first number in equation (float)
    y: second number in equation (float)
    op: operator ['+', "-", '*', '/'] (str)
    z: result (float)
    """

    def __init__(self, **kwargs):
        super(Ledger, self).__init__(**kwargs)
        self.col = 'x'
        self.row = 1
        self.df = pd.DataFrame(columns=['x', 'y', 'op', 'z'])
        self.df.loc[1] = {'x': 0, 'y': 0, 'op': '', 'z': 0}
        self.clear_button_src = 'assets/graphics/clear.png'

    def select(self, col: str):
        """select active column"""
        if col not in ['x', 'y', 'op', 'z']:
            print(f"[ WARNING ] Invalid column: {col}")
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
        self.refresh_ledger()

    def operation(self, op: str):
        """update operator column of current row and advance selection"""
        if op not in ['+', '-', '*', '/']:
            print(f"[ WARNING ] Invalid operator: {op}")
        print(self.df.at[self.row, 'op'])
        self.df.at[self.row, 'op'] = op
        self.select('y')
        self.refresh_ledger()

    def submit_row(self):
        """add and select new row at bottom of ledger"""
        self.col = 'z'
        # TODO: execute equation if possible and store result z
        print(self.df.loc[self.row])
        self.new_row()

    def refresh_ledger(self):
        """refresh ledger view with current data"""
        # TODO: Reincorporate A5's cuneiform translator commented out below (untested)
        rows = self.df.values.astype('str')
        self.rv.data = [
            {'value': row} for row in rows
        ]

    def new_row(self):
        """add and select new row at bottom of ledger"""
        index = len(self.df.index) + 1
        self.df.loc[index] = {'x': 0, 'y': 0, 'op': '', 'z': 0}
        self.row = index
        self.col = 'x'
        self.refresh_ledger()

    def clear(self):
        """clear ledger and backing dataframe"""
        self.df = pd.DataFrame(columns=['x', 'y', 'op', 'z'])
        self.new_row()

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
    #
    # def _keydown(self, *args):
    #     if(args[1] >= 257 and args[1] <= 265):
    #         if not self.add_left_digit(Image(source=f'assets/graphics/cuneiform/c{args[1] - 256}.png')):
    #             self.add_right_digit(Image(source=f'assets/graphics/cuneiform/c{args[1] - 256}.png'))
    #     if(args[1] == 267):
    #         l = Label(text="[color=000000]/[/color]", markup=True)
    #         l.font_size = '58dp'
    #         self.add_middle(l)
    #     if(args[1] == 268):
    #         l = Label(text="[color=000000]*[/color]", markup=True)
    #         l.font_size = '58dp'
    #         self.add_middle(l)
    #     if(args[1] == 269):
    #         l = Label(text="[color=000000]-[/color]", markup=True)
    #         l.font_size = '58dp'
    #         self.add_middle(l)
    #     if(args[1] == 270):
    #         l = Label(text="[color=000000]+[/color]", markup=True)
    #         l.font_size = '58dp'
    #         self.add_middle(l)
    #     if(args[1] == 271):
    #         self.l_pos = ''
    #         self.m_pos = ''
    #         self.r_pos = ''
    #         self.next_line()
