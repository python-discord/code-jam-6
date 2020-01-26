"""
Backend data frame to be displayed by the ledger.
"""

import pandas as pd

from .calculator import Calculator

# test_data = [
#     {'x': 3, 'y': 2, 'op': '*', 'z': 6},
#     {'x': 4, 'y': 8, 'op': '+', 'z': 12},
#     {'x': 0, 'y': 0, 'op': None, 'z': 0}
# ]
# ledger_df = pd.DataFrame(test_data)

ledger_df = pd.DataFrame(columns=['x', 'y', 'op', 'z'])

calculator = Calculator(df=ledger_df)
