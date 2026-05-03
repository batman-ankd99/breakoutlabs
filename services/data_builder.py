import pandas as pd


def build_dataset(df, symbol):
    try:
        if df is None or len(df) == 0:
            return None

        df = df.copy()

        # Normalize column names safely
        df.columns = [str(c).strip() for c in df.columns]

        # Ensure Close exists
        if "Close" not in df.columns:
            print(f"[BUILD] Missing Close for {symbol}")
            return None

        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.dropna(subset=["Close"])

        # Sort by time if Date exists
        if "Date" in df.columns:
            df = df.sort_values("Date")

        # returns
        df["return_3m"] = df["Close"].pct_change(63)
        df["return_6m"] = df["Close"].pct_change(126)
        df["return_12m"] = df["Close"].pct_change(252)

        df["symbol"] = symbol

        df = df.dropna()

        return df

    except Exception as e:
        print(f"build_dataset error: {e}")
        return None
