"""
Backend controller for communicating operations b/w widgets
"""

import pandas as pd
from .ledger import Ledger
from kivy.uix.widget import Widget


class Controller(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('[ INIT CONTROLLER ]')
        self.df = pd.DataFrame(columns=['x', 'y', 'op', 'z'])
        self.ledger = Ledger()
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
        rows = self.df.values
        print(f"ROWS: {rows}")
        self.ledger.refresh()


controller = Controller()
