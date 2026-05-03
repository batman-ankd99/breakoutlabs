import pandas as pd


def build_dataset(df: pd.DataFrame, symbol: str):

    if df is None or df.empty:
        print(f"[BUILD] empty input: {symbol}")
        return None

    df = df.copy()

    # normalize column names
    df.columns = [c.lower() for c in df.columns]

    # ensure close exists
    if "close" not in df.columns:
        print(f"[BUILD] Missing Close for {symbol}")
        print(f"[BUILD] Available columns: {df.columns}")
        return None

    # convert safely
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    # IMPORTANT: do NOT wipe full dataset
    df = df.dropna(subset=["close"])

    if len(df) < 50:
        print(f"[BUILD] Not enough valid data for {symbol}")
        return None

    # returns (momentum features)
    df["return_3m"] = df["close"].pct_change(63)
    df["return_6m"] = df["close"].pct_change(126)
    df["return_12m"] = df["close"].pct_change(252)

    # keep only valid rows for momentum
    df = df.dropna(subset=["return_3m", "return_6m", "return_12m"])

    if df.empty:
        print(f"[BUILD] All rows dropped after feature engineering: {symbol}")
        return None

    print(f"[BUILD OK] {symbol}: {len(df)} rows")

    return df
