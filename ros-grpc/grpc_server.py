import time
import grpc
from concurrent import futures

import ros_pb2
import ros_pb2_grpc

from .shared_data import shared


#  gRPC service

class RosGrpcGatewayService(ros_pb2_grpc.RosGrpcGatewayServicer):
    """
    Streams the latest chatter stored in SharedState.
    """

    def StreamChatter(self, request, context):
        last_seq = None

        while True:
            latest = shared.get_chatter()
            if latest and latest.get("seq") != last_seq:
                last_seq = latest.get("seq")
                yield ros_pb2.Chatter(
                    data=latest.get("data", ""),
                    seq=latest.get("seq", 0)
                )

            time.sleep(0.2)

# gRPC server bootstrap

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    ros_pb2_grpc.add_RosGrpcGatewayServicer_to_server(
        RosGrpcGatewayService(),
        server
    )

    server.add_insecure_port("[::]:50051")

    print("Starting gRPC server on port 50051...")

    server.start()

    print("gRPC server running on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()