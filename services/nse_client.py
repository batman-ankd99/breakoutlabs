import yfinance as yf
import pandas as pd


class NSEClient:

    def get_1y_history(self, symbol: str):
        try:
            ticker = symbol.replace("-EQ", "") + ".NS"
            print(f"Fetching: {ticker}")

            df = yf.download(
                ticker,
                period="1y",
                interval="1d",
                progress=False,
                auto_adjust=False,
                group_by="column"
            )

            if df is None or df.empty:
                print(f"[ERROR] No data for {symbol}")
                return None

            df = df.reset_index()

            # ✅ SAFE COLUMN NORMALIZER (handles tuple + string)
            cleaned_cols = []

            for c in df.columns:

                # tuple case → take first element
                if isinstance(c, tuple):
                    c = c[0]

                # string safety
                c = str(c).lower()

                cleaned_cols.append(c)

            df.columns = cleaned_cols

            # remove duplicates safely
            df = df.loc[:, ~df.columns.duplicated()]

            print(f"RAW OK {symbol}: {len(df)} rows")
            print(f"COLUMNS: {df.columns.tolist()}")

            return df

        except Exception as e:
            print(f"[NSE_CLIENT ERROR] {symbol}: {e}")
            return None
