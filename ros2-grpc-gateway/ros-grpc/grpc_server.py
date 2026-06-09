import time
import grpc
from concurrent import futures

import ros_pb2
import ros_pb2_grpc


class RosGrpcGateway(ros_pb2_grpc.RosGrpcGatewayServicer):

    def StreamChatter(self, request, context):
        """
        Server-side streaming:
        client sends 1 request → server streams many responses
        """

        seq = 0

        while True:
            yield ros_pb2.Chatter(
                data=f"Hello from ROS gRPC #{seq}",
                seq=seq
            )

            seq += 1
            time.sleep(1)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ros_pb2_grpc.add_RosGrpcGatewayServicer_to_server(RosGrpcGateway(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting gRPC server on port 50051...")
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()