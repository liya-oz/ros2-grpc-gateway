from flask import Flask, jsonify
import grpc
import ros_pb2
import ros_pb2_grpc

GRPC_HOST = "ros-grpc:50051"

app = Flask(__name__)

@app.get("/api/chatter")
def api_chatter():
    try:
        with grpc.insecure_channel(GRPC_HOST) as channel:
            stub = ros_pb2_grpc.RosGrpcGatewayStub(channel) #remote function caller

            responses = stub.StreamChatter(
                ros_pb2.Empty(),
                timeout=1
            )

            for resp in responses:
                return jsonify({
                    "data": resp.data,
                    "seq": resp.seq
                }), 200

    except Exception as e:
        return jsonify({
            "error": "gRPC unavailable",
            "details": str(e)
        }), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)