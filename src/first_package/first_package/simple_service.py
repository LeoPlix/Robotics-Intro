"""
ROS 2 service server node that adds two integers and returns their sum.
"""
import rclpy
from rclpy.node import Node
from first_interfaces.srv import ExampleService


class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.service = self.create_service(ExampleService, 'add_two_ints', self.handle_request)

    def handle_request(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Received request: {request.a} + {request.b} = {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
