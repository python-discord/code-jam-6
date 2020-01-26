"""
Backend calculator for storing values and communicating operations b/w widgets
"""

import pandas as pd


class Calculator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.col = 'x'
        self.row = 1
        self.new_row()
        print(f"Active Cell: {self.df.at[self.row, self.col]}")

    def update(self, n: int, op: str = '+'):
        """Update active cell"""
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

    def new_row(self):
        index = len(self.df.index) + 1
        self.df.loc[index] = {'x': 0, 'y': 0, 'op': None, 'z': 0}
        self.row = index
        self.col = 'x'
        print(self.df)
