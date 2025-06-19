# launch/finger_nav.launch.py

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='finger_nav',
            executable='finger_nav',
            name='finger_nav',
            output='screen'
        )
    ])

