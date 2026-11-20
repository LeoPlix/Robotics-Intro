# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/6_stm_serial_node_pub.py
# Template: Templates/7_stm_serial_node_pub_sub.py
# DONE marks code implementation, not a successful ROS/hardware test.
"""Runnable D1.1 and D1.2 checkpoints using standard ROS messages."""
from std_msgs.msg import Float32MultiArray

from .protocol import FIELDS, standard_control_values
from .serial_node import SerialNode, run_node


# 2. Define the SerialPublisherNode class
# 2. Define the SerialPubSubNode class
# ADAPTATION: SerialNode supplies the transport shared by both stages.
class StandardSerialNode(SerialNode):
    state_message_type = Float32MultiArray
    control_message_type = Float32MultiArray

    # DONE (template TODO): Create and populate the Float32MultiArray message
    # Create a Float32MultiArray message
    def state_message(self, values):
        msg = Float32MultiArray()
        # State field order is kept in protocol.FIELDS (the eight template variables).
        msg.data = [values[field] for field in FIELDS]
        return msg

    # D1.2 command callback delegates the four-array-field validation to protocol.py.
    def control_values(self, msg):
        return standard_control_values(msg.data)


# D1.1: template 6 publisher only (no stm_control subscription).
def publisher_main(args=None):
    run_node(lambda: StandardSerialNode(enable_control=False), args)


# D1.2: template 7 publisher plus subscriber; serial setup is inherited.
def pubsub_main(args=None):
    run_node(StandardSerialNode, args)
