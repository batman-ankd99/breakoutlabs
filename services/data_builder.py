import pandas as pd


def build_dataset(df, symbol):
    try:
        if df is None or len(df) == 0:
            return None

        df = df.copy()

        # normalize column names aggressively
        df.columns = [str(c).strip().lower() for c in df.columns]

        print(f"[BUILD] columns for {symbol}: {df.columns}")

        # 🔥 handle multiple possible Close variants
        close_col = None
        for c in df.columns:
            if "close" in c:
                close_col = c
                break

        if close_col is None:
            print(f"[BUILD] No Close-like column for {symbol}")
            return None

        df["close"] = pd.to_numeric(df[close_col], errors="coerce")
        df = df.dropna(subset=["close"])

        df = df.sort_values(by=df.columns[0])  # Date column usually first

        df["return_3m"] = df["close"].pct_change(63)
        df["return_6m"] = df["close"].pct_change(126)
        df["return_12m"] = df["close"].pct_change(252)

        df["symbol"] = symbol

        df = df.dropna()

        return df

    except Exception as e:
        print(f"build_dataset error: {e}")
        return None
