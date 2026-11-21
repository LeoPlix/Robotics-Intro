"""
Reactive Bug0 obstacle avoidance node using 2D LiDAR scans.
Segments LaserScan ranges into right, front, and left angular sectors,
evaluating clearances to generate forward drive or turning commands
published as TwistStamped (for simulation) and STMControl (for hardware).
"""
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
from stm_interfaces.msg import STMControl


class Bug0LidarSTMNode(Node):
    def __init__(self):
        super().__init__('bug0_lidar_stm_node')

        self.obstacle_distance = 1.0  # meters
        self.linear_speed = 0.3      # m/s
        self.angular_speed = 0.5     # rad/s
        self.forward_pwm = 90.0
        self.turn_pwm = 70.0

        self.scan_subscriber = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )
        self.sim_velocity_publisher = self.create_publisher(
            TwistStamped, '/diff_drive_controller/cmd_vel', 10
        )
        self.stm_control_publisher = self.create_publisher(
            STMControl, '/stm_control', 10
        )

        self.right_distance = float('inf')
        self.front_distance = float('inf')
        self.left_distance = float('inf')
        self.scan_received = False

        self.control_timer = self.create_timer(0.1, self.control_timer_callback)  # 10 Hz
        self.get_logger().info('Bug0 obstacle avoidance node initialized.')

    def get_min_distance(self, ranges_section):
        valid_ranges = [
            distance
            for distance in ranges_section
            if math.isfinite(distance) and distance > 0.05
        ]
        return min(valid_ranges) if valid_ranges else float('inf')

    def scan_callback(self, msg):
        total_points = len(msg.ranges)
        section_size = total_points // 3

        right_ranges = msg.ranges[:section_size]
        front_ranges = msg.ranges[section_size:2 * section_size]
        left_ranges = msg.ranges[2 * section_size:]

        self.right_distance = self.get_min_distance(right_ranges)
        self.front_distance = self.get_min_distance(front_ranges)
        self.left_distance = self.get_min_distance(left_ranges)
        self.scan_received = True

    def control_timer_callback(self):
        if not self.scan_received:
            return

        sim_cmd = TwistStamped()
        stm_cmd = STMControl()

        stamp = self.get_clock().now().to_msg()
        sim_cmd.header.stamp = stamp
        stm_cmd.header.stamp = stamp

        stm_cmd.control_type = 2
        stm_cmd.setpoint = 0.0
        stm_cmd.kp = 0.0

        # Bug0 reactive navigation: drive forward if clear, turn towards clearer side if blocked
        if self.front_distance > self.obstacle_distance:
            sim_cmd.twist.linear.x = self.linear_speed
            sim_cmd.twist.angular.z = 0.0
            stm_cmd.pwm = self.forward_pwm
        else:
            sim_cmd.twist.linear.x = 0.0
            if self.left_distance >= self.right_distance:
                sim_cmd.twist.angular.z = self.angular_speed
                stm_cmd.pwm = self.turn_pwm
            else:
                sim_cmd.twist.angular.z = -self.angular_speed
                stm_cmd.pwm = -self.turn_pwm

        self.sim_velocity_publisher.publish(sim_cmd)
        self.stm_control_publisher.publish(stm_cmd)

        self.get_logger().info(
            f"Sectors - Right: {self.right_distance:.2f}m, Front: {self.front_distance:.2f}m, Left: {self.left_distance:.2f}m"
        )


def main(args=None):
    rclpy.init(args=args)
    bug0_lidar_stm_node = Bug0LidarSTMNode()

    try:
        rclpy.spin(bug0_lidar_stm_node)
    except KeyboardInterrupt:
        pass
    finally:
        bug0_lidar_stm_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
