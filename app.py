from flask import Flask, jsonify
from services.nse_client import NSEClient
from services.data_builder import build_dataset
from services.momentum_engine import calculate_momentum

app = Flask(__name__)
client = NSEClient()

SYMBOLS = [
    "RELIANCE-EQ",
    "TCS-EQ",
    "INFY-EQ",
    "HDFCBANK-EQ",
    "ICICIBANK-EQ"
]


@app.route("/momentum/top")
def top_momentum():

    results = []

    for s in SYMBOLS:

        # 1. Fetch data
        raw = client.get_1y_history(s)
        if raw is None:
            continue

        # 2. Build dataset
        clean = build_dataset(raw, s)
        if clean is None or len(clean) == 0:
            continue

        # 3. Momentum scoring
        scored = calculate_momentum(clean)

        if scored is None or scored.empty:
            continue

        # 4. IMPORTANT FIX:
        # pick TOP momentum row (not last row)
        top_row = scored.iloc[0]

        if "momentum_score" not in top_row:
            continue

        results.append({
            "symbol": s,
            "score": float(top_row["momentum_score"])
        })

    # 5. sort final output
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # 6. safe response
    if not results:
        return jsonify({
            "status": "error",
            "message": "No stock data fetched"
        }), 500

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
