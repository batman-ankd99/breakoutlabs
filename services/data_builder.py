import pandas as pd


def build_dataset(df: pd.DataFrame, symbol: str):
    try:
        if df is None or df.empty:
            print(f"[BUILD] empty input: {symbol}")
            return None

        df = df.copy()

        # normalize
        df.columns = [c.lower().strip() for c in df.columns]

        # ensure sorting (VERY IMPORTANT)
        if "date" in df.columns:
            df = df.sort_values("date")

        if "close" not in df.columns:
            print(f"[BUILD] missing close: {symbol}")
            return None

        # force numeric (critical safety fix)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")

        # returns
        df["return_3m"] = df["close"].pct_change(63)
        df["return_6m"] = df["close"].pct_change(126)
        df["return_12m"] = df["close"].pct_change(252)

        # 🔥 IMPORTANT FIX: don't wipe everything
        df = df.dropna(subset=["return_3m", "return_6m", "return_12m"])

        print(f"[BUILD OK] {symbol}: {len(df)} rows after features")

        if len(df) < 5:
            print(f"[BUILD] not enough usable rows: {symbol}")
            return None

        return df

    except Exception as e:
        print(f"[BUILD ERROR] {symbol}: {e}")
        return None
