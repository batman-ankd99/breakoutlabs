import pandas as pd


def calculate_momentum(df):

    # 🔥 SAFETY CHECK
    required = {"Close"}
    if not required.issubset(df.columns):
        raise ValueError(f"Expected raw OHLC data, got: {df.columns}")

    df = df.copy().reset_index(drop=True)

    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # RETURNS
    df["return_12m"] = df["Close"] / df["Close"].shift(252) - 1
    df["return_6m"]  = df["Close"] / df["Close"].shift(126) - 1
    df["return_3m"]  = df["Close"] / df["Close"].shift(63) - 1

    df = df.dropna(subset=["return_12m", "return_6m", "return_3m"])

    # SCORE
    df["momentum_score"] = (
        0.5 * df["return_12m"] +
        0.3 * df["return_6m"] +
        0.2 * df["return_3m"]
    )

    return df.sort_values("momentum_score", ascending=False)
