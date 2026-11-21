"""
Launch description for running a standalone STM serial communication bridge.
"""
import os
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('stm_station')
    serial_params = os.path.join(share_dir, 'config', 'serial_params.yaml')

    params = yaml.safe_load(open(serial_params))
    namespace = f"group_{params['/**']['ros__parameters']['group_id']}"

    return LaunchDescription([
        Node(
            package='stm_station',
            executable='stm_serial_node',
            namespace=namespace,
            name='stm_serial_node',
            parameters=[serial_params],
            output='screen',
        ),
    ])
