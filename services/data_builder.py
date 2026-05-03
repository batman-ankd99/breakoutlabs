import pandas as pd


def build_dataset(df: pd.DataFrame, symbol: str):
    try:
        if df is None or df.empty:
            return None

        df = df.copy()

        # flatten safety (again defensive)
        df.columns = [str(c).lower().strip() for c in df.columns]

        # handle both formats safely
        close_col = None
        for c in df.columns:
            if "close" in c:
                close_col = c
                break

        if close_col is None:
            print(f"[BUILD] No close column found: {symbol}")
            print(f"[BUILD] Columns: {df.columns}")
            return None

        df["return_3m"] = df[close_col].pct_change(63)
        df["return_6m"] = df[close_col].pct_change(126)
        df["return_12m"] = df[close_col].pct_change(252)

        df = df.dropna(subset=["return_3m", "return_6m", "return_12m"])

        if len(df) < 10:
            return None

        print(f"[BUILD OK] {symbol}: {len(df)} rows")

        return df

    except Exception as e:
        print(f"[BUILD ERROR] {symbol}: {e}")
        return None
