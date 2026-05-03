import yfinance as yf
import pandas as pd


class NSEClient:

    def get_1y_history(self, symbol: str):
        try:
            ticker = symbol.replace("-EQ", "") + ".NS"
            print(f"Fetching: {ticker}")

            df = yf.download(ticker, period="1y", progress=False, group_by="column")

            if df is None or df.empty:
                print(f"[ERROR] No data for {symbol}")
                return None

            df = df.reset_index()

            # 🔥 CRITICAL FIX: flatten multi-index columns
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [
                    col[0].lower() if isinstance(col, tuple) else str(col).lower()
                    for col in df.columns
                ]
            else:
                df.columns = [str(c).lower() for c in df.columns]

            print(f"RAW OK {symbol}: {len(df)} rows")
            print(f"COLUMNS: {df.columns.tolist()}")

            return df

        except Exception as e:
            print(f"[NSE_CLIENT ERROR] {symbol}: {e}")
            return None
