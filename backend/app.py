from flask import Flask, jsonify
import os
import requests

BRIDGE_URL = os.getenv("BRIDGE_URL", "http://ros2:9090")

app = Flask(__name__)

@app.get("/api/chatter")
def api_chatter():
    r = requests.get(f"{BRIDGE_URL}/latest/chatter", timeout=1)
    return jsonify(r.json()), r.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)