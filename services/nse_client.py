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

            # 🚨 CRITICAL FIX: flatten ALL column types
            df.columns = [
                c.split(".")[0].lower() if "." in str(c) else str(c).lower()
                for c in df.columns
            ]

            # sometimes yfinance adds weird duplicates → clean again
            df = df.loc[:, ~df.columns.duplicated()]

            print(f"RAW OK {symbol}: {len(df)} rows")
            print(f"COLUMNS: {df.columns.tolist()}")

            return df

        except Exception as e:
            print(f"[NSE_CLIENT ERROR] {symbol}: {e}")
            return None
