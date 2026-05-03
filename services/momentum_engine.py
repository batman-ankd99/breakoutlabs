import pandas as pd


def calculate_momentum(df):
    df = df.reset_index(drop=True)

    # -------------------------
    # FIX: handle multi-index columns
    # -------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # -------------------------
    # FIX: safe column detection
    # -------------------------
    if "Close" not in df.columns:
        if "Adj Close" in df.columns:
            df["Close"] = df["Adj Close"]
        else:
            raise KeyError(f"No Close column found. Columns: {df.columns}")

    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # -------------------------
    # RETURNS
    # -------------------------
    df["return_12m"] = (df["Close"] / df["Close"].shift(252)) - 1
    df["return_6m"]  = (df["Close"] / df["Close"].shift(126)) - 1
    df["return_3m"]  = (df["Close"] / df["Close"].shift(63)) - 1

    df = df.dropna(subset=["return_12m", "return_6m", "return_3m"])

    # -------------------------
    # SCORE
    # -------------------------
    df["momentum_score"] = (
        0.5 * df["return_12m"] +
        0.3 * df["return_6m"] +
        0.2 * df["return_3m"]
    )

    return df.sort_values("momentum_score", ascending=False)
