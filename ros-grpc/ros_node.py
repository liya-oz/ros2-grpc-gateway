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


    def _on_message(self, msg: String) -> None:
        """
        Callback executed every time a message arrives.
        """

        # Minimal work in callback: store latest message safely
        seq = 0
        try:
            seq = int(msg.header.stamp.sec)
        except Exception:
            pass

        shared.update_chatter(msg.data, seq)
        self.get_logger().debug('Stored latest chatter message')


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