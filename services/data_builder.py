def build_dataset(df, symbol):
    """
    ONLY cleaning + validation.
    NO calculations here.
    """

    if df is None or df.empty:
        return None

    df = df.copy()
    df["symbol"] = symbol

    required = ["Date", "Open", "High", "Low", "Close", "Volume"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df = df[required + ["symbol"]]
    df = df.sort_values("Date").reset_index(drop=True)

    return df
