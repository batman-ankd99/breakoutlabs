import pandas as pd

def get_mock_stocks():
    data = [
        {"symbol": "RELIANCE", "return_12m": 55, "return_6m": 20, "return_3m": 10},
        {"symbol": "TCS", "return_12m": 40, "return_6m": 18, "return_3m": 8},
        {"symbol": "INFY", "return_12m": 60, "return_6m": 25, "return_3m": 12},
    ]
    return pd.DataFrame(data)
