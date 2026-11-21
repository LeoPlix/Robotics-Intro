"""
Closed-loop master-slave position controller using proportional PWM control.
Computes position error between master and slave actuators and generates
proportional PWM drive commands with saturation limits.
"""
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from stm_interfaces.msg import STMState, STMControl
from stm_interfaces.srv import STMSetControlType


class STMControlNode(Node):
    def __init__(self):
        super().__init__('stm_control_node')

        self.add_on_set_parameters_callback(self.parameter_callback)

        self.declare_parameter('master_group_id', 1)
        self.declare_parameter('slave_group_id', 2)
        self.loop_frequency = 50  # Hz

        self.master_group_id = self.get_parameter('master_group_id').value
        self.slave_group_id = self.get_parameter('slave_group_id').value

        self.master_state_topic = f"/group_{self.master_group_id}/stm_state"
        self.slave_state_topic = f"/group_{self.slave_group_id}/stm_state"
        self.slave_control_topic = f"/group_{self.slave_group_id}/stm_control"

        self.master_stm_state_subscriber = self.create_subscription(
            STMState, self.master_state_topic, self.master_stm_state_callback, 10
        )
        self.slave_stm_state_subscriber = self.create_subscription(
            STMState, self.slave_state_topic, self.slave_stm_state_callback, 10
        )
        self.get_logger().info(f"Subscribed to master: {self.master_state_topic}")
        self.get_logger().info(f"Subscribed to slave: {self.slave_state_topic}")

        self.slave_stm_control_publisher = self.create_publisher(
            STMControl, self.slave_control_topic, 10
        )
        self.get_logger().info(f"Publishing to slave control: {self.slave_control_topic}")

        self.control_type_service_name = 'set_control_type'
        self.control_type_service = self.create_service(
            STMSetControlType, self.control_type_service_name, self.service_control_type_callback
        )

        self.timer_control_loop = self.create_timer(1.0 / self.loop_frequency, self.timer_callback)

        self.master_position = 0.0
        self.slave_position = 0.0
        self.control_type = 0  # 0: Stop, 1: Onboard position, 2: Closed-loop PWM P-control
        self.kp = 1.0

    def master_stm_state_callback(self, msg):
        self.master_position = msg.motor_encoder

    def slave_stm_state_callback(self, msg):
        self.slave_position = msg.motor_encoder

    def service_control_type_callback(self, request, response):
        """
        Sets control mode (0: Stop, 1: Onboard position, 2: Closed-loop P-control).
        """
        self.control_type = request.control_type if request.control_type in (0, 1, 2) else 0

        if request.kp >= 0.0:
            self.kp = request.kp
        else:
            self.kp = 0.0
            self.get_logger().warning(f"Invalid control gain kp={request.kp}; defaulting to {self.kp}")

        self.get_logger().info(f"Control type set to {self.control_type}, kp={self.kp}")
        response.success = True
        return response

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'master_group_id':
                self.master_group_id = param.value
                self.master_state_topic = f"/group_{self.master_group_id}/stm_state"
                if hasattr(self, 'master_stm_state_subscriber'):
                    self.destroy_subscription(self.master_stm_state_subscriber)
                    self.master_stm_state_subscriber = self.create_subscription(
                        STMState, self.master_state_topic, self.master_stm_state_callback, 10
                    )
                    self.get_logger().info(f"Updated master subscriber to: {self.master_state_topic}")

            elif param.name == 'slave_group_id':
                self.slave_group_id = param.value
                self.slave_state_topic = f"/group_{self.slave_group_id}/stm_state"
                if hasattr(self, "slave_stm_state_subscriber"):
                    self.destroy_subscription(self.slave_stm_state_subscriber)
                    self.slave_stm_state_subscriber = self.create_subscription(
                        STMState, self.slave_state_topic, self.slave_stm_state_callback, 10
                    )
                self.slave_control_topic = f"/group_{self.slave_group_id}/stm_control"
                if hasattr(self, 'slave_stm_control_publisher'):
                    self.destroy_publisher(self.slave_stm_control_publisher)
                    self.slave_stm_control_publisher = self.create_publisher(
                        STMControl, self.slave_control_topic, 10
                    )
                    self.get_logger().info(f"Updated slave publisher to: {self.slave_control_topic}")

        return SetParametersResult(successful=True)

    def timer_callback(self):
        control_msg = STMControl()

        if 0 <= self.control_type <= 2:
            error = self.master_position - self.slave_position
            control_command = self.kp * error
            pwm_limit = 250.0
            control_command = max(-pwm_limit, min(pwm_limit, control_command))

            control_msg.control_type = self.control_type
            control_msg.kp = self.kp
            control_msg.setpoint = self.master_position
            control_msg.pwm = control_command if self.control_type == 2 else 0.0
        else:
            self.get_logger().warning(f"Unknown control type: {self.control_type}")
            control_msg.control_type = 0
            control_msg.kp = 0.0
            control_msg.setpoint = 0.0

        self.slave_stm_control_publisher.publish(control_msg)
        self.get_logger().info(f"Published control command: {control_msg}")


def main(args=None):
    rclpy.init(args=args)
    stm_control_node = STMControlNode()

    try:
        rclpy.spin(stm_control_node)
    except KeyboardInterrupt:
        pass
    finally:
        stm_control_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
