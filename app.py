from flask import Flask, jsonify
import pandas as pd

from services.data_builder import build_dataset
from services.momentum_engine import calculate_momentum

app = Flask(__name__)

# ---------------------------
# Health Check
# ---------------------------
@app.route("/")
def home():
    return jsonify({
        "service": "MomentumAI",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# ---------------------------
# Momentum Screener API
# ---------------------------
@app.route("/momentum/top")
def top_momentum():
    try:
        # Step 1: build dataset from NSE
        data = build_dataset()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No stock data fetched"
            })

        # Step 2: convert to DataFrame
        df = pd.DataFrame(data)

        # Step 3: calculate momentum score + ranking
        ranked_df = calculate_momentum(df)

        # Step 4: return top results
        top_stocks = ranked_df.head(20)

        return jsonify({
            "status": "success",
            "count": len(top_stocks),
            "data": top_stocks.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# ---------------------------
# Run Server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
