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

        raw = equity_history(symbol, "EQ")

        print("RAW RESPONSE TYPE:", type(raw))
        print("RAW RESPONSE:", raw)

        return None  # stop pipeline for debugging

    except Exception as e:
        print(f"ERROR: {e}")
        return None
