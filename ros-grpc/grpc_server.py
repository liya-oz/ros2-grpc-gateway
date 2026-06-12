import time
import threading
import grpc
from concurrent import futures
from dataclasses import dataclass

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import ros_pb2
import ros_pb2_grpc


@dataclass(frozen=True) #immutable data class 
class ChatterState:
    data: str = ""
    seq: int = 0


class State:
    def __init__(self):
        self._lock = threading.Lock()
        self._latest = ChatterState()

    def update(self, data: str, seq: int) -> None:
        with self._lock:
            self._latest = ChatterState(data=data, seq=seq)

    def get(self) -> ChatterState:
        with self._lock:
            return ChatterState(data=self._latest.data, seq=self._latest.seq)


state = State()


class ChatterSubscriber(Node):

    def __init__(self) -> None:
        super().__init__("chatter_subscriber")
        self._seq = 0
        self.create_subscription(String, "chatter", self._on_msg, 10)
        self.get_logger().info("ROS subscriber started")

    def _on_msg(self, msg: String) -> None:
        self._seq += 1
        state.update(msg.data, self._seq)
        self.get_logger().info(f"Received: {msg.data} (seq={self._seq})")


def start_ros() -> None:
    rclpy.init()
    node = ChatterSubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


class GatewayService(ros_pb2_grpc.RosGrpcGatewayServicer):

    def StreamChatter(self, request, context):
        last_seq = 0
        while context.is_active():
            latest = state.get()
            if latest and latest.seq != last_seq:
                last_seq = latest.seq
                yield ros_pb2.Chatter(data=latest.data, seq=last_seq)
            time.sleep(0.5)


def serve_grpc() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    ros_pb2_grpc.add_RosGrpcGatewayServicer_to_server(GatewayService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server started on 50051")
    server.start()
    server.wait_for_termination()


def main() -> None:
    ros_thread = threading.Thread(target=start_ros, daemon=True)
    ros_thread.start()
    serve_grpc()


if __name__ == "__main__":
    main()