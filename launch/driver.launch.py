from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Locate parameter file
    PKG = get_package_share_directory('controller_commands')
    params_file = f'{PKG}/config/params.yaml'

    # Construct Launch Description
    LD = LaunchDescription()

    # Joy Driver
    LD.add_action(Node(package='controller_commands',
                       executable='joy_driver.py',
                       name='joy_driver',
                       parameters=[params_file]
                       ))

    # Joy Node
    LD.add_action(Node(package='joy',
                       executable='joy_node',
                       name='joy_node'))

    return LD
