import time
import grpc
from concurrent import futures #for gRPC server thread pool

import ros_pb2
import ros_pb2_grpc

from .shared_data import shared


class RosGrpcGatewayService(ros_pb2_grpc.RosGrpcGatewayServicer):
    """
    Streams the latest chatter stored in SharedState.
    """

    def StreamChatter(self, request, context):
        last_seq = None

        while context.is_active(): # Check if client is still connected
            latest = shared.get_chatter()
            if latest and latest.get("seq") != last_seq: # Only send if there's a new message
                last_seq = latest.get("seq")
                yield ros_pb2.Chatter(
                    data=latest.get("data", ""),
                    seq=latest.get("seq", 0)
                )

            time.sleep(0.5) #fine for mvp, use threading.Event or similar for more efficient cpu

# gRPC server bootstrap
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

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