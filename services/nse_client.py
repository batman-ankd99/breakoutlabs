from nsepython import nse_eq, equity_history
from datetime import date, timedelta
import pandas as pd


class NSEClient:

    # -----------------------------
    # LIVE QUOTE
    # -----------------------------
    def get_quote(self, symbol):
        try:
            data = nse_eq(symbol)
            return data.get("priceInfo", {})
        except Exception as e:
            print(f"Quote error for {symbol}: {e}")
            return None

    # -----------------------------
    # 1 YEAR HISTORY (FIXED)
    # -----------------------------
    def get_1y_history(self, symbol):
        try:
            print(f"Fetching history: {symbol}")

            end_date = date.today()
            start_date = end_date - timedelta(days=365)

            # ✅ CORRECT SIGNATURE FOR YOUR ENVIRONMENT
            data = equity_history(
                symbol,
                "EQ",
                start_date.strftime("%d-%m-%Y"),
                end_date.strftime("%d-%m-%Y")
            )

            if data is None:
                print(f"No data returned for {symbol}")
                return None

            # Normalize response safely
            if isinstance(data, dict) and "data" in data:
                df = pd.DataFrame(data["data"])
            else:
                df = pd.DataFrame(data)

            if df is None or df.empty:
                print(f"Empty dataframe for {symbol}")
                return None

            print(f"SUCCESS {symbol}: {len(df)} rows")
            return df

        except Exception as e:
            print(f"ERROR for {symbol}: {e}")
            return None
