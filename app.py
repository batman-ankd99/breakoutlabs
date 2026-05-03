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

    try:
        results = []

        for s in SYMBOLS:

            print(f"\n--- Processing {s} ---")

            raw = client.get_1y_history(s)
            if raw is None:
                print(f"RAW None: {s}")
                continue

            clean = build_dataset(raw, s)
            if clean is None or clean.empty:
                print(f"CLEAN empty: {s}")
                continue

            scored = calculate_momentum(clean)

            if scored is None:
                print(f"SCORED None: {s}")
                continue

            if scored.empty:
                print(f"SCORED empty: {s}")
                continue

            print(f"SCORING OK {s}: {len(scored)} rows")

            top_row = scored.iloc[0]

            results.append({
                "symbol": s,
                "score": float(top_row["momentum_score"])
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        print("\nFINAL RESULTS:", results)

        if not results:
            return jsonify({
                "status": "error",
                "message": "No stock data fetched"
            }), 500

        return jsonify(results)

    except Exception as e:
        print("\n🔥 FLASK CRASH ERROR:", str(e))
        import traceback
        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
