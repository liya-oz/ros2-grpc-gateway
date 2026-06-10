import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    """
    Minimal ROS2 publisher node.
    Publishes a counter message at fixed interval.
    """

    def __init__(self) -> None:
        super().__init__('talker')

        self.pub = self.create_publisher(
            String,
            'chatter',
            10
        )

        self.count = 0

        self.timer = self.create_timer(
            0.5,
            self._on_tick
        )

        self.get_logger().info('Talker node started')

    def _on_tick(self) -> None:
        msg = String()
        msg.data = f'Hello #{self.count}'
        self.pub.publish(msg)

        self.get_logger().info(
            f'Publishing: {msg.data}'
        )

        self.count += 1


def main(args=None) -> None:
    rclpy.init(args=args)

    node = Talker()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info(
            'Shutting down Talker node'
        )

    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()