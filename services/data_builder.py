import pandas as pd


def build_dataset(df: pd.DataFrame, symbol: str):
    try:
        if df is None or df.empty:
            return None

        df = df.copy()

        # normalize columns
        df.columns = [c.lower().strip() for c in df.columns]

        # handle missing close
        if "close" not in df.columns:
            print(f"[BUILD] missing close: {symbol}")
            print(f"[BUILD] columns: {df.columns}")
            return None

        # numeric conversion
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df = df.dropna(subset=["close"])

        # FIX: robust date handling
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.sort_values("date")
        else:
            df = df.sort_index()

        # 🔥 FIXED WINDOWS (IMPORTANT)
        # based on trading days (~252/year)
        w3 = 63     # 3 months
        w6 = 126    # 6 months
        w12 = 189   # ~9 months (safer than 252 for 1y data)

        df["return_3m"] = df["close"].pct_change(w3)
        df["return_6m"] = df["close"].pct_change(w6)
        df["return_12m"] = df["close"].pct_change(w12)

        # only drop rows where ALL signals are missing
        df = df.dropna(subset=["return_3m", "return_6m", "return_12m"])

        if len(df) < 20:
            print(f"[BUILD] not enough usable rows: {symbol}")
            return None

        print(f"[BUILD OK] {symbol}: {len(df)} rows after features")

        return df

    except Exception as e:
        print(f"[BUILD ERROR] {symbol}: {e}")
        return None
