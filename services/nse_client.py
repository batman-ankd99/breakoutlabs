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

            # IMPORTANT: flatten index issues
            df = df.reset_index()

            # Ensure standard columns exist
            if "Close" not in df.columns:
                print(f"No Close column for {symbol}, columns: {df.columns}")
                return None

            print(f"RAW OK {symbol}: {len(df)} rows")
            return df

        except Exception as e:
            print(f"ERROR: {e}")
            return None
