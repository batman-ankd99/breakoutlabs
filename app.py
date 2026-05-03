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


@app.route("/")
def home():
    return jsonify({"service": "breakoutlabs", "status": "running"})


@app.route("/momentum/top")
def top_momentum():

    market = client.get_market_history()
    if market is None:
        return jsonify({"error": "market data failed"}), 500

    results = []

    for s in SYMBOLS:

        stock = client.get_stock_history(s)
        if stock is None:
            continue

        clean = build_dataset(stock, s)
        if clean is None:
            continue

        scored = calculate_momentum(clean, market)

        if scored is None or scored.empty:
            continue

        latest = scored.iloc[-1]

        results.append({
            "symbol": s,
            "score": float(latest["momentum_score"])
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
