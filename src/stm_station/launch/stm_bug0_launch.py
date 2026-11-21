"""
Launch description for the reactive Bug0 LiDAR-based obstacle avoidance node.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='stm_station',
            executable='bug0_lidar_stm_node',
            output='screen',
        )
    ])
