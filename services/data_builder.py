from services.nse_client import NSEClient
from services.universe import get_universe

client = NSEClient()

def build_dataset():
    stocks = get_universe()
    data = []

    for s in stocks:
        try:
            history = client.get_1y_history(s)

            if history is None or len(history) < 2:
                continue

            start = history.iloc[0]["CH_CLOSING_PRICE"]
            end = history.iloc[-1]["CH_CLOSING_PRICE"]

            return_12m = ((end - start) / start) * 100

            data.append({
                "symbol": s,
                "return_12m": return_12m,
                "return_6m": return_12m * 0.6,   # placeholder for now
                "return_3m": return_12m * 0.3    # placeholder for now
            })

        except Exception as e:
            print(f"Error {s}: {e}")

    return data
