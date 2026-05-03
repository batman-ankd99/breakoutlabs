import pandas as pd


def build_dataset(df, symbol):

    if df is None or df.empty:
        print(f"[BUILD] empty input: {symbol}")
        return None

    df = df.copy()

    # normalize
    df.columns = [c.lower() for c in df.columns]

    # FINAL SAFETY: fix close column variants
    close_col = None

    for c in df.columns:
        if "close" in c:
            close_col = c
            break

    if close_col is None:
        print(f"[BUILD] No close column found for {symbol}")
        print(f"[BUILD] Columns: {df.columns}")
        return None

    df["close"] = pd.to_numeric(df[close_col], errors="coerce")
    df = df.dropna(subset=["close"])

    if len(df) < 50:
        print(f"[BUILD] Not enough data: {symbol}")
        return None

    # returns
    df["return_3m"] = df["close"].pct_change(63)
    df["return_6m"] = df["close"].pct_change(126)
    df["return_12m"] = df["close"].pct_change(252)

    df = df.dropna()

    print(f"[BUILD OK] {symbol}: {len(df)} rows")

    return df
