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
                auto_adjust=False
            )

            if df is None or df.empty:
                print(f"[ERROR] No data for {symbol}")
                return None

            # Reset index so Date becomes column
            df = df.reset_index()

            # Flatten columns (VERY IMPORTANT for yfinance edge cases)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip() for col in df.columns.values]

            # Normalize column names
            df.columns = [c.lower().replace(" ", "_") for c in df.columns]

            print(f"RAW OK {symbol}: {len(df)} rows")
            print(f"COLUMNS: {df.columns.tolist()}")

            return df

        except Exception as e:
            print(f"[NSE_CLIENT ERROR] {symbol}: {e}")
            return None
