"""
ROS 2 forwarding node combining subscriber and publisher functionality
using custom message types.
"""
import rclpy
from rclpy.node import Node
from first_interfaces.msg import ExampleMessage


class PubSubNode(Node):
    def __init__(self):
        super().__init__('pubsub_7')
        self.publisher = self.create_publisher(ExampleMessage, 'topic_7_out', 10)
        self.subscription = self.create_subscription(
            ExampleMessage, 'topic_7', self.listener_callback, 10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'Forwarding message: {msg}')
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PubSubNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
