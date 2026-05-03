from nsepython import nse_eq, equity_history
from datetime import date, timedelta

class NSEClient:

    def get_quote(self, symbol):
        data = nse_eq(symbol)
        return data["priceInfo"]

    def get_1y_history(self, symbol):
        end = date.today()
        start = end - timedelta(days=365)

        return equity_history(
            symbol,
            start.strftime("%d-%m-%Y"),
            end.strftime("%d-%m-%Y")
        )

    def get_1y_history(self, symbol):
    try:
        print(f"Fetching: {symbol}")

        end = date.today()
        start = end - timedelta(days=365)

        data = equity_history(
            symbol,
            start.strftime("%d-%m-%Y"),
            end.strftime("%d-%m-%Y")
        )

        print(f"Got data for {symbol}: {len(data)} rows")

        return data

    except Exception as e:
        print(f"ERROR for {symbol}: {e}")
        return None    
