import json
import os

from services.nse_client import NSEClient
from services.data_builder import build_dataset
from services.momentum_engine import calculate_momentum
from data.nifty500 import NIFTY500

client = NSEClient()

results = []

for s in NIFTY500:
    print(f"\nProcessing {s}")

    raw = client.get_1y_history(s)
    if raw is None:
        continue

    clean = build_dataset(raw, s)
    if clean is None or clean.empty:
        continue

    scored = calculate_momentum(clean)
    if scored is None or scored.empty:
        continue

    latest = scored.iloc[-1]

    results.append({
        "symbol": s,
        "score": float(latest["momentum_score"])
    })

results = sorted(results, key=lambda x: x["score"], reverse=True)

os.makedirs("data", exist_ok=True)

with open("data/momentum_output.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved results → data/momentum_output.json")
