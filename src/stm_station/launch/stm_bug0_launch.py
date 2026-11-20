# Course basis: Launch-Pattern + Vorlage 13; no direct template.
# Changes: see docs/TEMPLATE_CHANGES.md.
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([Node(package='stm_station', executable='bug0_lidar_stm_node', output='screen')])
