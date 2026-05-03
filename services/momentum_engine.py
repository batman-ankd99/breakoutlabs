# services/momentum_engine.py
import pandas as pd


def calculate_momentum(df):
    try:
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.copy()

        # safety: ensure numeric
        for col in ["return_12m", "return_6m", "return_3m"]:
            if col not in df.columns:
                df[col] = 0.0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        df["momentum_score"] = (
            0.5 * df["return_12m"] +
            0.3 * df["return_6m"] +
            0.2 * df["return_3m"]
        )

        df = df.dropna(subset=["momentum_score"])

        if df.empty:
            return pd.DataFrame()

        return df.sort_values("momentum_score", ascending=False)

    except Exception as e:
        print(f"[MOMENTUM ERROR] {e}")
        return pd.DataFrame()
