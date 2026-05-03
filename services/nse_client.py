from nsepython import nse_eq, equity_history
from datetime import date, timedelta
import pandas as pd


class NSEClient:

    def get_quote(self, symbol):
        try:
            data = nse_eq(symbol)
            return data.get("priceInfo", {})
        except Exception as e:
            print(f"Quote error: {e}")
            return None

    def get_1y_history(self, symbol):
        try:
            print(f"Fetching history: {symbol}")

            end_date = date.today()
            start_date = end_date - timedelta(days=365)

            raw = equity_history(
                symbol,
                "EQ",
                start_date.strftime("%d-%m-%Y"),
                end_date.strftime("%d-%m-%Y")
            )

            if raw is None:
                print(f"No raw data for {symbol}")
                return None

            # -----------------------------
            # Normalize ALL possible formats
            # -----------------------------

            if isinstance(raw, dict) and "data" in raw:
                data = raw["data"]
            else:
                data = raw

            if not data:
                print(f"Empty dataset for {symbol}")
                return None

            df = pd.DataFrame(data)

            print(f"Got {symbol}: {len(df)} rows")
            return df

        except Exception as e:
            print(f"ERROR for {symbol}: {e}")
            return None
