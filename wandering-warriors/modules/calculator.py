"""
Backend calculator for storing values and communicating operations b/w widgets
"""


class Calculator:
    def __init__(self):
        self.active_value = 0
        self.active_operator = None
        self.tab_value = 0

    def add(self, x: int):
        self.active_value = self.active_value + x

    def subtract(self, x: int):
        self.active_value = self.active_value - x

    def multiply(self, x: int):
        self.active_value = self.active_value * x

    def divide(self, x: int):
        self.active_value = self.active_value / x

    def tabulate(self, x: int):
        # For tabulating growing base-60 values from drawpad
        self.tab_value = self.tab_value + x
