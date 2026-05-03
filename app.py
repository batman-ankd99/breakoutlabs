from flask import Flask, jsonify, render_template
import subprocess
import json
import os

app = Flask(__name__)

DATA_FILE = "data/momentum_output.json"


# ---------------- UI ----------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ---------------- API: latest data ----------------
@app.route("/api/momentum/latest")
def latest_momentum():
    if not os.path.exists(DATA_FILE):
        return jsonify({"status": "no_data"})

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    return jsonify(data)


# ---------------- API: RUN BUTTON ----------------
@app.route("/api/momentum/run", methods=["POST"])
def run_momentum():
    try:
        # run your job script
        result = subprocess.run(
            ["python3", "jobs/run_momentum.py"],
            capture_output=True,
            text=True
        )

        return jsonify({
            "status": "ok",
            "output": result.stdout[-1000:]  # last logs
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
