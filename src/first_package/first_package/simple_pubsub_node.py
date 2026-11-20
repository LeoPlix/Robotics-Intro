# Course basis: Vorlagen 1 + 2, kombiniert; no direct template.
# Changes: see docs/TEMPLATE_CHANGES.md.
# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/1_simple_publisher.py
# Template: Templates/2_simple_subscriber.py
# DONE marks code implementation, not a successful ROS/hardware test.
import rclpy
from rclpy.node import Node
from first_interfaces.msg import ExampleMessage

# Step 1: Define a class for the publisher node
# Step 1: Define a class for the subscriber node
# ADAPTATION: Combine the publisher/subscriber roles in a forwarding node.
class PubSubNode(Node):
    def __init__(self):
        super().__init__('pubsub_7')
        # Step 2: Create a publisher for your topic
        self.publisher = self.create_publisher(ExampleMessage, 'topic_7_out', 10)
        # Step 2: Create a subscription to your group's topic
        self.subscription = self.create_subscription(
            ExampleMessage, 'topic_7', self.listener_callback, 10
        )

    # Step 3: Define the callback function that will be called when a message is received
    def listener_callback(self, msg):
        # Log the received message to the console
        self.get_logger().info(f'Weiterleiten: {msg}')
        # Publish the message
        self.publisher.publish(msg)



# Define the main function to run the node
def main(args=None):
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)
    node = PubSubNode()
    try:
        # Run the node until interrupted
        rclpy.spin(node)
    # Gracefully handle shutdown when Ctrl+C is pressed
    except KeyboardInterrupt:
        pass
    finally:
        # Destroy the node and shutdown the ROS2 Python client library
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()


