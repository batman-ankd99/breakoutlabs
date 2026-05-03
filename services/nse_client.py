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
    # 1 YEAR HISTORY (FIXED + ROBUST)
    # -----------------------------
    def get_1y_history(self, symbol):
        try:
            print(f"Fetching history: {symbol}")

            end_date = date.today()
            start_date = end_date - timedelta(days=365)

            # IMPORTANT: NSE expects "EQ"
            raw = equity_history(
                symbol,
                "EQ",
                start_date.strftime("%d-%m-%Y"),
                end_date.strftime("%d-%m-%Y")
            )

            # -----------------------------
            # SAFETY CHECK 1
            # -----------------------------
            if raw is None:
                print(f"No data returned for {symbol}")
                return None

            # -----------------------------
            # SAFETY CHECK 2: DataFrame case
            # -----------------------------
            if hasattr(raw, "empty"):
                df = raw

            # -----------------------------
            # SAFETY CHECK 3: dict case
            # -----------------------------
            elif isinstance(raw, dict):
                if "data" in raw:
                    df = pd.DataFrame(raw["data"])
                else:
                    df = pd.DataFrame(raw)

            # -----------------------------
            # SAFETY CHECK 4: list case
            # -----------------------------
            else:
                df = pd.DataFrame(raw)

            # -----------------------------
            # FINAL VALIDATION
            # -----------------------------
            if df is None or df.empty:
                print(f"Empty dataframe for {symbol}")
                return None

            print(f"SUCCESS {symbol}: {len(df)} rows")
            return df

        except Exception as e:
            print(f"ERROR for {symbol}: {e}")
            return None
