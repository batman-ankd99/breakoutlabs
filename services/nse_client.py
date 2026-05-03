import yfinance as yf
import pandas as pd


class NSEClient:

    def _to_symbol(self, symbol):
        return symbol.replace("-EQ", "") + ".NS"

    def get_stock_history(self, symbol):
        try:
            ticker = self._to_symbol(symbol)
            print(f"Fetching stock: {ticker}")

            df = yf.download(ticker, period="1y", auto_adjust=False)

            if df is None or df.empty:
                return None

            df = df.reset_index()
            return df

        except Exception as e:
            print(f"Stock error {symbol}: {e}")
            return None

    def get_market_history(self):
        try:
            print("Fetching market: ^NSEI")

            df = yf.download("^NSEI", period="1y", auto_adjust=False)

            if df is None or df.empty:
                return None

            df = df.reset_index()
            return df

        except Exception as e:
            print(f"Market error: {e}")
            return None
