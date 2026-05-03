import pandas as pd


def calculate_momentum(df: pd.DataFrame):
    try:
        if df is None or df.empty:
            return None

        df = df.copy()

        required = ["return_12m", "return_6m", "return_3m"]
        for r in required:
            if r not in df.columns:
                print(f"[MOMENTUM] missing column {r}")
                return None

        df["momentum_score"] = (
            0.5 * df["return_12m"] +
            0.3 * df["return_6m"] +
            0.2 * df["return_3m"]
        )

        df = df.dropna(subset=["momentum_score"])

        return df.sort_values("momentum_score")

    except Exception as e:
        print(f"[MOMENTUM ERROR] {e}")
        return None
