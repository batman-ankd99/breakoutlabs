import pandas as pd


def build_dataset(df, symbol):
    """
    ONLY ensures schema consistency.
    NO returns calculation here.
    """

    if df is None or df.empty:
        return None

    df = df.copy()
    df["symbol"] = symbol

    required_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing {col} in dataset")

    df = df[required_cols + ["symbol"]]

    df = df.sort_values("Date").reset_index(drop=True)

    return df
