import pandas as pd
import numpy as np


def calculate_momentum(stock_df, market_df):

    stock_df = stock_df.copy().reset_index(drop=True)
    market_df = market_df.copy().reset_index(drop=True)

    stock_df["Close"] = pd.to_numeric(stock_df["Close"], errors="coerce")
    market_df["Close"] = pd.to_numeric(market_df["Close"], errors="coerce")

    # -------------------------
    # RETURNS
    # -------------------------
    stock_df["ret_1y"] = stock_df["Close"] / stock_df["Close"].shift(180)
    market_df["ret_1y_mkt"] = market_df["Close"] / market_df["Close"].shift(180)

    stock_df["rel_strength"] = stock_df["ret_1y"] / market_df["ret_1y_mkt"]

    # -------------------------
    # SHORT TERM MOMENTUM
    # -------------------------
    stock_df["ret_3m"] = stock_df["Close"] / stock_df["Close"].shift(45)

    # -------------------------
    # VOLATILITY
    # -------------------------
    stock_df["volatility"] = stock_df["Close"].pct_change().rolling(20).std()

    stock_df = stock_df.dropna()

    # -------------------------
    # FINAL SCORE (RELATIVE MOMENTUM)
    # -------------------------
    stock_df["momentum_score"] = (
        0.6 * stock_df["rel_strength"] +
        0.3 * stock_df["ret_3m"] +
        0.1 * stock_df["Close"].pct_change().rolling(20).mean()
    ) / (stock_df["volatility"] + 1e-6)

    # convert to percentile ranking
    stock_df["momentum_score"] = stock_df["momentum_score"].rank(pct=True)

    return stock_df.sort_values("momentum_score", ascending=False)
