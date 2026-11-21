"""
Serial communication node using standard Float32MultiArray messages.
"""
from std_msgs.msg import Float32MultiArray

from .protocol import FIELDS, standard_control_values
from .serial_node import SerialNode, run_node


class StandardSerialNode(SerialNode):
    state_message_type = Float32MultiArray
    control_message_type = Float32MultiArray

    def state_message(self, values):
        msg = Float32MultiArray()
        msg.data = [values[field] for field in FIELDS]
        return msg

    def control_values(self, msg):
        return standard_control_values(msg.data)


def publisher_main(args=None):
    run_node(lambda: StandardSerialNode(enable_control=False), args)


def pubsub_main(args=None):
    run_node(StandardSerialNode, args)
