import pandas as pd


def build_dataset(df: pd.DataFrame, symbol: str):
    try:
        if df is None or df.empty:
            print(f"[BUILD] empty input: {symbol}")
            return None

        df = df.copy()

        # standardise column names
        df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

        # ensure required columns exist
        if "close" not in df.columns:
            print(f"[BUILD] Missing close column: {symbol}")
            print(f"[BUILD] Available columns: {df.columns}")
            return None

        df = df.sort_values("date" if "date" in df.columns else df.columns[0])

        # returns (safe)
        df["return_3m"] = df["close"].pct_change(63)
        df["return_6m"] = df["close"].pct_change(126)
        df["return_12m"] = df["close"].pct_change(252)

        # IMPORTANT FIX: do NOT nuke dataset
        df = df.dropna(subset=["return_3m", "return_6m", "return_12m"])

        if len(df) < 10:
            print(f"[BUILD] Not enough data after feature engineering: {symbol}")
            return None

        print(f"[BUILD OK] {symbol}: {len(df)} rows")

        return df

    except Exception as e:
        print(f"[BUILD ERROR] {symbol}: {e}")
        return None
