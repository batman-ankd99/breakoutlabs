from flask import Flask, jsonify
from services.nse_client import NSEClient
from services.data_builder import build_dataset
from services.momentum_engine import calculate_momentum
from flask import render_template

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
def dashboard():
    return render_template("dashboard.html")

@app.route("/momentum/top")
def top_momentum():

    results = []

    for s in SYMBOLS:
        print(f"\n--- Processing {s} ---")

        raw = client.get_1y_history(s)
        if raw is None:
            continue

        clean = build_dataset(raw, s)
        if clean is None or clean.empty:
            print(f"CLEAN empty: {s}")
            continue

        scored = calculate_momentum(clean)
        if scored is None or scored.empty:
            continue

        latest = scored.iloc[-1]

        results.append({
            "symbol": s,
            "score": float(latest["momentum_score"])
        })

    if not results:
        return jsonify({
            "status": "error",
            "message": "No stock data fetched"
        }), 500

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return jsonify(results)

@app.route("/momentum/run", methods=["POST"])
def run_momentum():
    results = []

    for s in NIFTY500:
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
    with open("data/momentum_cache.json", "w") as f:
        json.dump(results, f, indent=2)

    return jsonify({
        "status": "success",
        "count": len(results)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
