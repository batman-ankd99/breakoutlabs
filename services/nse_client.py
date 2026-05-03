import yfinance as yf
import pandas as pd


class NSEClient:

    def _to_symbol(self, symbol):
        return symbol.replace("-EQ", "") + ".NS"

    def get_1y_history(self, symbol):
        try:
            ticker = self._to_symbol(symbol)
            print(f"Fetching: {ticker}")

            df = yf.download(ticker, period="1y", auto_adjust=False)

            if df is None or df.empty:
                print(f"No data for {symbol}")
                return None

            # FIX: flatten columns if needed
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df = df.reset_index()

            print(f"RAW OK {symbol}: {len(df)} rows")
            return df

        except Exception as e:
            print(f"ERROR {symbol}: {e}")
            return None
