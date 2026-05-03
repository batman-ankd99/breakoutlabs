import pandas as pd


def build_dataset(df: pd.DataFrame, symbol: str):
    try:
        if df is None or df.empty:
            return None

        df = df.copy()

        # normalize
        df.columns = [c.lower().strip() for c in df.columns]

        if "close" not in df.columns:
            print(f"[BUILD] missing close: {symbol}")
            return None

        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df = df.dropna(subset=["close"])

        df = df.sort_values("date") if "date" in df.columns else df

        n = len(df)

        # 🔥 adaptive windows (KEY FIX)
        w3 = min(20, max(5, int(n * 0.1)))
        w6 = min(50, max(10, int(n * 0.25)))
        w12 = min(100, max(20, int(n * 0.5)))

        df["return_3m"] = df["close"].pct_change(w3)
        df["return_6m"] = df["close"].pct_change(w6)
        df["return_12m"] = df["close"].pct_change(w12)

        # safe cleanup (not destructive anymore)
        df = df.dropna(subset=["return_3m", "return_6m", "return_12m"])

        if len(df) < 10:
            print(f"[BUILD] not enough usable rows: {symbol}")
            return None

        print(f"[BUILD OK] {symbol}: {len(df)} rows after features")

        return df

    except Exception as e:
        print(f"[BUILD ERROR] {symbol}: {e}")
        return None
