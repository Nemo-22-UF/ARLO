from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config_dir = os.path.join(get_package_share_directory('arlobot'), 'config')
    urdf_file = os.path.join(get_package_share_directory('arlobot'), 'urdf', 'arlo.urdf')

    return LaunchDescription([
        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            arguments=[urdf_file],
        ),

        # Motor Controller
        Node(
            package='arlobot',
            executable='motor_controller',
            name='motor_controller',
            output='screen'
        ),

        # Encoder Logger
        Node(
            package='arlobot',
            executable='encoder_logger',
            name='encoder_logger',
            output='screen'
        ),

        # Odometry Node
        Node(
            package='arlobot',
            executable='odom_node',
            name='odom_node',
            output='screen'
        ),

        # RPLIDAR Node
        Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            name='rplidar_node',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'serial_baudrate': 115200,
                'frame_id': 'laser',
                'inverted': False,
                'angle_compensate': True
            }]
        ),

        # SLAM Toolbox
        Node(
            package='slam_toolbox',
            executable='sync_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[os.path.join(config_dir, 'slam_toolbox_params.yaml')],
        ),

        # Nav2 Bringup
        Node(
            package='nav2_bringup',
            executable='bringup_launch.py',
            name='nav2_bringup',
            output='screen',
            parameters=[
                os.path.join(config_dir, 'nav2_params.yaml'),
                os.path.join(config_dir, 'costmap_common_params.yaml'),
                os.path.join(config_dir, 'global_costmap_params.yaml'),
                os.path.join(config_dir, 'local_costmap_params.yaml'),
                os.path.join(config_dir, 'base_local_planner_params.yaml'),
                os.path.join(config_dir, 'move_base_params.yaml'),
                {'use_sim_time': False}
            ]
        ),
    ])
