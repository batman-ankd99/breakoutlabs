import pandas as pd


def build_dataset(df, symbol):
    if df is None or df.empty:
        return None

    df = df.copy()
    df["symbol"] = symbol

    required = ["Date", "Open", "High", "Low", "Close", "Volume"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column {col}")

    return df[required + ["symbol"]].sort_values("Date")
