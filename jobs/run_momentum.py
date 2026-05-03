import sys
import os

# ✅ FIX: must come BEFORE imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.nse_client import NSEClient
from services.data_builder import build_dataset
from services.momentum_engine import calculate_momentum
from data.nifty500 import NIFTY500

import json
import time

client = NSEClient()
results = []

success = 0
fail = 0

for s in NIFTY500:
    print(f"\n--- Processing {s} ---")

    raw = client.get_1y_history(s)
    if raw is None:
        print(f"[FAIL] No raw data: {s}")
        fail += 1
        continue

    clean = build_dataset(raw, s)
    if clean is None or clean.empty:
        print(f"[FAIL] No clean data: {s}")
        fail += 1
        continue

    scored = calculate_momentum(clean)
    if scored is None or scored.empty:
        print(f"[FAIL] No momentum: {s}")
        fail += 1
        continue

    latest = scored.iloc[-1]

    results.append({
        "symbol": s,
        "score": float(latest["momentum_score"])
    })

    success += 1

    # ✅ prevent Yahoo throttling
    time.sleep(0.3)

# sort results
results = sorted(results, key=lambda x: x["score"], reverse=True)

print("\n==========================")
print(f"SUCCESS: {success}")
print(f"FAILED: {fail}")
print("==========================\n")

# save output
output_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "momentum_output.json"
)

with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"Saved results → {output_path}")
