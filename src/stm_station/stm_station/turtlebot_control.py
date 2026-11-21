"""
ROS 2 mobile robot teleoperation node.
Subscribes to STMState telemetry (motor velocity and gyroscope yaw rate)
and publishes Twist velocity commands to '/cmd_vel'.
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from stm_interfaces.msg import STMState


class STMTurtleBotControlNode(Node):
    def __init__(self):
        super().__init__('stm_turtlebot_control_node')

        self.declare_parameter('group_id', 1)
        self.group_id = self.get_parameter('group_id').get_parameter_value().integer_value

        stm_state_topic = f'/group_{self.group_id}/stm_state'
        self.stm_state_subscriber = self.create_subscription(
            STMState, stm_state_topic, self.stm_state_callback, 10
        )

        self.twist_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info(f"Subscribed to {stm_state_topic} and publishing to /cmd_vel")

    def stm_state_callback(self, msg):
        twist = Twist()

        # Map rotational velocity to linear velocity (wheel radius 0.033m, 24 ticks/rev, 9.7 ratio)
        twist.linear.x = msg.motor_velocity * 2 * 3.141592653589793 * 0.033 / (24 * 9.7)
        twist.angular.z = msg.gyro_z

        self.twist_publisher.publish(twist)
        self.get_logger().info(f"Published linear={twist.linear.x:.3f}, angular={twist.angular.z:.3f}")


def main(args=None):
    rclpy.init(args=args)
    node = STMTurtleBotControlNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
