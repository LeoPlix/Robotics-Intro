"""
ROS 2 node that reads IMU and encoder data from a microcontroller via serial
and publishes it as a standard Float32MultiArray on 'stm_state'.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import serial


class SerialPublisherNode(Node):
    def __init__(self):
        super().__init__('stm_serial_node')

        self.port = '/dev/ttyACM0'
        self.baudrate = 115200
        self.loop_frequency = 1000  # Hz

        self.serial_port = serial.Serial(self.port, self.baudrate, timeout=0.01)
        self.get_logger().info(f'Initialized serial communication on {self.port} at {self.baudrate} baud.')

        self.stm_state_topic = 'stm_state'
        self.stm_state_publisher = self.create_publisher(Float32MultiArray, self.stm_state_topic, 10)

        self.timer = self.create_timer(1.0 / self.loop_frequency, self.timer_read_pub_callback)

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
                    msg = Float32MultiArray()
                    msg.data = float_values
                    self.stm_state_publisher.publish(msg)

                self.get_logger().info(f'Published state: {float_values}')
            except ValueError as e:
                self.get_logger().warn(f'Error parsing serial data: {e}')

    def destroy_node(self):
        self.serial_port.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SerialPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
