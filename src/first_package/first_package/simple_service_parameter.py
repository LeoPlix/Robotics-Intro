"""
ROS 2 service node with dynamic parameter reconfiguration.
Calculates the sum of two integers plus an extra configurable term.
"""
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from first_interfaces.srv import ExampleService


class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')

        self.add_on_set_parameters_callback(self.parameter_callback)
        self.declare_parameter('extra_term', 10)
        self.extra_term = self.get_parameter('extra_term').get_parameter_value().integer_value

        self.service = self.create_service(ExampleService, 'add_two_ints', self.handle_request)

    def handle_request(self, request, response):
        response.sum = request.a + request.b + self.extra_term
        self.get_logger().info(
            f'Received request: {request.a} + {request.b} + {self.extra_term} = {response.sum}'
        )
        return response

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'extra_term':
                self.extra_term = param.value
                self.get_logger().info(f"Updated extra_term to: {self.extra_term}")

        return SetParametersResult(successful=True, reason="Parameters updated successfully.")


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
