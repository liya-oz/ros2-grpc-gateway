from flask import Flask, jsonify
import os
import requests
import grpc

import ros_pb2
import ros_pb2_grpc

BRIDGE_URL = os.getenv("BRIDGE_URL", "http://ros2:9090")
GRPC_HOST = os.getenv("GRPC_HOST", "ros-grpc:50051")

app = Flask(__name__)


@app.get("/api/chatter")
def api_chatter():
    # Try gRPC first
    try:
        with grpc.insecure_channel(GRPC_HOST) as channel:
            stub = ros_pb2_grpc.RosGrpcGatewayStub(channel)
            # StreamChatter is a server-streaming RPC; take the first yielded message
            responses = stub.StreamChatter(ros_pb2.Empty(), timeout=1)
            for resp in responses:
                return jsonify({"data": resp.data, "seq": resp.seq}), 200
    except Exception:
        pass

    # Fallback to HTTP bridge
    r = requests.get(f"{BRIDGE_URL}/latest/chatter", timeout=1)
    return jsonify(r.json()), r.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)