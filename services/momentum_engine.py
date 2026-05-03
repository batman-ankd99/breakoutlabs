import pandas as pd

def calculate_momentum(df):
    df["momentum_score"] = (
        0.5 * df["return_12m"] +
        0.3 * df["return_6m"] +
        0.2 * df["return_3m"]
    )

    return df.sort_values("momentum_score", ascending=False)
