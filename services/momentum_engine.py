import pandas as pd
import numpy as np


def calculate_momentum(df):

    if "Close" not in df.columns:
        raise ValueError(f"Missing Close column: {df.columns}")

    df = df.copy().reset_index(drop=True)
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # -------------------------
    # RETURNS (log-based better)
    # -------------------------
    df["ret_1y"] = np.log(df["Close"] / df["Close"].shift(180))
    df["ret_6m"] = np.log(df["Close"] / df["Close"].shift(90))
    df["ret_3m"] = np.log(df["Close"] / df["Close"].shift(45))

    # -------------------------
    # VOLATILITY (risk penalty)
    # -------------------------
    df["volatility"] = df["Close"].pct_change().rolling(20).std()

    df = df.dropna()

    # -------------------------
    # MOMENTUM SCORE (RISK ADJUSTED)
    # -------------------------
    df["momentum_score"] = (
        0.5 * df["ret_1y"] +
        0.3 * df["ret_6m"] +
        0.2 * df["ret_3m"]
    ) / (df["volatility"] + 1e-6)

    # -------------------------
    # CLEAN NORMALIZATION
    # -------------------------
    df["momentum_score"] = (
        df["momentum_score"] - df["momentum_score"].mean()
    ) / df["momentum_score"].std()

    return df.sort_values("momentum_score", ascending=False)
