import grpc

import ros_pb2
import ros_pb2_grpc


# Connect to gRPC server
channel = grpc.insecure_channel(
    "localhost:50051"
)


# Create client stub
stub = ros_pb2_grpc.RosGrpcGatewayStub(
    channel
)


# Call streaming RPC
messages = stub.StreamChatter(
    ros_pb2.Empty()
)


for msg in messages:
    print(
        f"Received: data={msg.data}, seq={msg.seq}"
    )
