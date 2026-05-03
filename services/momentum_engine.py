def calculate_momentum(df):

    if df is None or df.empty:
        return df

    df = df.copy()

    required = ["return_12m", "return_6m", "return_3m"]

    for col in required:
        if col not in df.columns:
            print(f"[MOMENTUM] missing {col}")
            return df

    df["momentum_score"] = (
        0.5 * df["return_12m"] +
        0.3 * df["return_6m"] +
        0.2 * df["return_3m"]
    )

    return df.sort_values("momentum_score", ascending=False)
