import pandas as pd


def calculate_momentum(df):
    # 🔥 FIX 1: force clean index alignment
    df = df.reset_index(drop=True)

    # 🔥 FIX 2: ensure numeric safety
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # -------------------------
    # RETURNS (SAFE CALCULATION)
    # -------------------------

    df["return_12m"] = (df["Close"] / df["Close"].shift(252)) - 1
    df["return_6m"]  = (df["Close"] / df["Close"].shift(126)) - 1
    df["return_3m"]  = (df["Close"] / df["Close"].shift(63)) - 1

    # 🔥 FIX 3: remove NaN rows before scoring
    df = df.dropna(subset=["return_12m", "return_6m", "return_3m"])

    # -------------------------
    # MOMENTUM SCORE
    # -------------------------
    df["momentum_score"] = (
        0.5 * df["return_12m"] +
        0.3 * df["return_6m"] +
        0.2 * df["return_3m"]
    )

    # 🔥 FIX 4: reset again for safety before sorting
    df = df.reset_index(drop=True)

    return df.sort_values("momentum_score", ascending=False)
