import pandas as pd


def calculate_momentum(stock_df):
    try:
        if stock_df is None or stock_df.empty:
            return pd.DataFrame()

        df = stock_df.copy()

        for col in ["return_12m", "return_6m", "return_3m"]:
            if col not in df.columns:
                df[col] = 0.0

        df["momentum_score"] = (
            0.5 * df["return_12m"] +
            0.3 * df["return_6m"] +
            0.2 * df["return_3m"]
        )

        return df.sort_values("momentum_score", ascending=False)

    except Exception as e:
        print(f"momentum error: {e}")
        return pd.DataFrame()
