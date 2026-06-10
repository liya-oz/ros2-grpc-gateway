import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from .shared_data import shared


class ChatterSubscriber(Node):
    """
    Minimal ROS2 subscriber node.
    Receives String messages from chatter topic.
    """

    def __init__(self) -> None:
        super().__init__('chatter_subscriber')

        self.subscription = self.create_subscription(
            String,
            'chatter',
            self._on_message,
            10
        )

        self.get_logger().info('ChatterSubscriber started"')


    def _on_message(self, msg: String) -> None:
        """
        Callback executed every time a message arrives.
        """
        self._seq += 1
        data = msg.data
        shared.update_chatter(data, self._seq)


def main(args=None) -> None:
    rclpy.init(args=args)

    node = ChatterSubscriber()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info(
            'Shutting down ChatterSubscriber node'
        )

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()