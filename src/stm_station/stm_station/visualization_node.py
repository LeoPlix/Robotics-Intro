"""
Telemetry state estimation and TF transform broadcaster node for RViz.
Subscribes to STMState, estimates orientation from wheel encoder ticks,
integrates linear acceleration for position tracking, and broadcasts
the dynamic TF tree (world -> group_id/stm_station).
"""
import math
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from tf_transformations import quaternion_from_euler
from stm_interfaces.msg import STMState


class STMVisualizationNode(Node):
    def __init__(self):
        super().__init__('stm_visualization_node')

        self.declare_parameter('group_id', 7)
        self.group_id = self.get_parameter('group_id').value

        input_topic = f'/group_{self.group_id}/stm_state'

        self.position = [0.0, 0.0, 0.0]
        self.velocity = [0.0, 0.0, 0.0]
        self.rotation = 0.0
        self.first_reading = True
        self.offset_acceleration = np.array([0.0, 0.0, 0.0])
        self.last_time = self.get_clock().now()

        self.data_subscriber = self.create_subscription(
            STMState, input_topic, self.stm_state_callback, 10
        )
        self.tf_broadcaster = TransformBroadcaster(self)

        self.get_logger().info(f"Broadcasting TF transforms for {input_topic}")

    def stm_state_callback(self, msg):
        linear_acceleration = np.array([msg.accel_x, msg.accel_y, msg.accel_z])

        # Convert encoder ticks to radians (24 ticks/rev, 9.7 gear ratio)
        self.rotation = msg.motor_encoder * 2 * math.pi / (24 * 9.7)

        # Baseline acceleration calibration on initial sample
        if self.first_reading:
            self.first_reading = False
            self.offset_acceleration = linear_acceleration.copy()

        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds * 1e-9
        self.last_time = current_time

        corrected_accel = linear_acceleration - self.offset_acceleration

        # Deadband threshold to reduce integration drift
        threshold = 0.5
        if np.linalg.norm(corrected_accel) > threshold:
            for i in range(3):
                self.velocity[i] += corrected_accel[i] * dt
                self.position[i] += self.velocity[i] * dt

        self.broadcast_transform()

    def broadcast_transform(self):
        transform = TransformStamped()

        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'world'
        transform.child_frame_id = f'group_{self.group_id}/stm_station'

        transform.transform.translation.x = self.position[0]
        transform.transform.translation.y = self.position[1]
        transform.transform.translation.z = self.position[2]

        quaternion = quaternion_from_euler(0.0, 0.0, self.rotation)
        transform.transform.rotation.x = quaternion[0]
        transform.transform.rotation.y = quaternion[1]
        transform.transform.rotation.z = quaternion[2]
        transform.transform.rotation.w = quaternion[3]

        self.tf_broadcaster.sendTransform(transform)
        self.get_logger().info(
            f"Broadcasted TF: position={self.position}, yaw={self.rotation:.3f} rad"
        )


def main(args=None):
    rclpy.init(args=args)
    stm_visualization_node = STMVisualizationNode()

    try:
        rclpy.spin(stm_visualization_node)
    except KeyboardInterrupt:
        pass
    finally:
        stm_visualization_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
