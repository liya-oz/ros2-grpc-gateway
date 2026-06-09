import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    """
    Minimal ROS2 subscriber node.
    Receives String messages from chatter topic.
    """

    def __init__(self) -> None:
        super().__init__('listener')

        self.subscription = self.create_subscription(
            String,
            'chatter',
            self._on_message,
            10
        )

        self.get_logger().info('Listener node started')


    def _on_message(self, msg: String) -> None:
        """
        Callback executed every time a message arrives.
        """

        self.get_logger().info(
            f'Received: {msg.data}'
        )


def main(args=None) -> None:
    rclpy.init(args=args)

    node = Listener()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info(
            'Shutting down Listener node'
        )

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()