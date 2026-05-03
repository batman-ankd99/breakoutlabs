from nsepython import nse_eq, equity_history
from datetime import date, timedelta


class NSEClient:

    # -----------------------------
    # Get live quote
    # -----------------------------
    def get_quote(self, symbol):
        try:
            data = nse_eq(symbol)
            return data.get("priceInfo", {})
        except Exception as e:
            print(f"Quote error for {symbol}: {e}")
            return None

    # -----------------------------
    # Get 1Y historical data
    # -----------------------------
    def get_1y_history(self, symbol):
        try:
            print(f"Fetching history: {symbol}")

            end_date = date.today()
            start_date = end_date - timedelta(days=365)

            data = equity_history(
                symbol,
                start_date.strftime("%d-%m-%Y"),
                end_date.strftime("%d-%m-%Y")
            )

            if data is None:
                print(f"No data returned for {symbol}")
                return None

            print(f"Got {symbol}: {len(data)} rows")
            return data

        except Exception as e:
            print(f"ERROR for {symbol}: {e}")
            return None
