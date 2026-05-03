from services.nse_client import NSEClient
from services.data_builder import build_dataset
from services.momentum_engine import calculate_momentum


client = NSEClient()

symbols = ["RELIANCE-EQ", "TCS-EQ", "INFY-EQ"]

results = []

for s in symbols:
    raw = client.get_1y_history(s)
    clean = build_dataset(raw, s)

    if clean is None:
        continue

    scored = calculate_momentum(clean)

    # take latest score
    latest = scored.iloc[-1]

    results.append({
        "symbol": s,
        "score": float(latest["momentum_score"])
    })

results = sorted(results, key=lambda x: x["score"], reverse=True)

print(results)
