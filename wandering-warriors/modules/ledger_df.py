"""
Backend data frame to be displayed by the ledger.
"""

import pandas as pd

test_data = [
    {'val1': 3, 'op': '*', 'val2': 2, 'res': 6},
    {'val1': 4, 'op': '+', 'val2': 8, 'res': 12},
    {'val1': 0, 'op': None, 'val2': 0, 'res': 0}
]

df = pd.DataFrame(test_data)
