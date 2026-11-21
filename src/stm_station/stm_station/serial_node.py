"""
Hardware serial bridge node using custom STMState and STMControl interfaces.
Reads sensor telemetry from serial and publishes timestamped STMState messages,
and translates received STMControl commands into framed serial packets.
"""
import rclpy
from rclpy.node import Node
from stm_interfaces.msg import STMState, STMControl
import serial


class SerialPubSubNode(Node):
    def __init__(self):
        super().__init__('stm_serial_node')

        self.port = self.declare_parameter('serial_port', '/dev/ttyACM0').value
        self.baudrate = self.declare_parameter('baud_rate', 115200).value
        self.loop_frequency = 1000  # Hz

        self.serial_port = serial.Serial(self.port, self.baudrate, timeout=0.01)
        self.get_logger().info(f'Initialized serial communication on {self.port} at {self.baudrate} baud.')

        self.stm_state_topic = 'stm_state'
        self.stm_state_publisher = self.create_publisher(STMState, self.stm_state_topic, 10)

        self.timer = self.create_timer(1.0 / self.loop_frequency, self.timer_read_pub_callback)

        self.stm_control_topic = 'stm_control'
        self.stm_control_subscriber = self.create_subscription(
            STMControl, self.stm_control_topic, self.stm_control_callback, 10
        )

    def timer_read_pub_callback(self):
        if self.serial_port.in_waiting > 0:
            try:
                serial_data_raw = self.serial_port.readline()
                serial_data_decoded = serial_data_raw.decode('utf-8')
                serial_data = serial_data_decoded.strip()

                # Expected frame format: {pos, vel, ax, ay, az, gx, gy, gz}
                if serial_data.startswith('{') and serial_data.endswith('}'):
                    serial_data = serial_data[1:-1]
                else:
                    self.get_logger().warn('Incoming serial data is missing brace delimiters')
                    return

                string_float_values = serial_data.split(',')
                float_values = [float(value) for value in string_float_values]

                if len(float_values) == 8:
                    msg = STMState()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.motor_encoder = float_values[0]
                    msg.motor_velocity = float_values[1]
                    msg.accel_x = float_values[2]
                    msg.accel_y = float_values[3]
                    msg.accel_z = float_values[4]
                    msg.gyro_x = float_values[5]
                    msg.gyro_y = float_values[6]
                    msg.gyro_z = float_values[7]

                    self.stm_state_publisher.publish(msg)

                self.get_logger().info(f'Published state: {float_values}')
            except ValueError as e:
                self.get_logger().warn(f'Error parsing serial data: {e}')

    def stm_control_callback(self, msg):
        """
        Receives an STMControl message and formats it into the serial packet:
        '{control_type, setpoint, kp, pwm}\\n'
        """
        try:
            control_data = f"{{{int(msg.control_type)}, {msg.setpoint}, {msg.kp}, {msg.pwm}}}\n"
            self.serial_port.write(control_data.encode('utf-8'))
            self.get_logger().info(f'Sent control command: {control_data.strip()}')
        except Exception as e:
            self.get_logger().error(f'Error sending control command: {e}')

    def destroy_node(self):
        self.serial_port.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SerialPubSubNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
