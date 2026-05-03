import yfinance as yf


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

            df = yf.download(ticker, period="1y")

            if df is None or df.empty:
                print(f"No data for {symbol}")
                return None

            print(f"SUCCESS {symbol}: {len(df)} rows")
            return df

        except Exception as e:
            print(f"ERROR: {e}")
            return None
