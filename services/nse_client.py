import yfinance as yf
import pandas as pd


class NSEClient:

    def get_quote(self, symbol):
        try:
            ticker = symbol.replace("-EQ", "") + ".NS"
            data = yf.Ticker(ticker).info
            return data
        except Exception as e:
            print(f"Quote error: {e}")
            return None

    def get_1y_history(self, symbol):
        try:
            ticker = symbol.replace("-EQ", "") + ".NS"
            print(f"Fetching: {ticker}")

            df = yf.download(ticker, period="1y", progress=False)

            if df is None or df.empty:
                print(f"No data for {symbol}")
                return None

            # 🔥 CRITICAL FIX: flatten columns (THIS WAS THE BUG)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # strip spaces just in case
            df.columns = [str(c).strip() for c in df.columns]

            df = df.reset_index()

            print(f"RAW OK {symbol}: {len(df)} rows")
            print(f"COLUMNS: {list(df.columns)}")

            return df

        except Exception as e:
            print(f"ERROR: {e}")
            return None
