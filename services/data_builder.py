import pandas as pd


def build_dataset(df, symbol):

    if df is None or df.empty:
        print(f"[BUILD] empty input: {symbol}")
        return None

    df = df.copy()
    df.columns = [str(c).lower() for c in df.columns]

    # find close column
    close_col = None
    for c in df.columns:
        if "close" in c:
            close_col = c
            break

    if close_col is None:
        print(f"[BUILD] No close column for {symbol}")
        return None

    df["close"] = pd.to_numeric(df[close_col], errors="coerce")
    df = df.dropna(subset=["close"])

    if len(df) < 100:
        print(f"[BUILD] Not enough raw data: {symbol}")
        return None

    # returns
    df["return_3m"] = df["close"].pct_change(63)
    df["return_6m"] = df["close"].pct_change(126)
    df["return_12m"] = df["close"].pct_change(252)

    # 🚨 IMPORTANT FIX: DO NOT DROP ALL NA ROWS
    # keep valid rows only for momentum calculation window
    df = df.dropna(subset=["return_12m", "return_6m", "return_3m"])

    if df.empty:
        print(f"[BUILD] All rows dropped after feature engineering: {symbol}")
        return None

    print(f"[BUILD OK] {symbol}: {len(df)} rows")

    return df
