#!/bin/bash
S="source /opt/ros/humble/setup.bash && source ~/arlobot_ws/install/setup.bash"
~/stop_arlo.sh
pkill -f rviz2 2>/dev/null
sleep 2
tmux new-session -d -s arlo -n lidar "bash -c '$S && ros2 launch rplidar_ros rplidar_a1_launch.py serial_port:=/dev/ttyUSB0 frame_id:=rplidar; exec bash'"
sleep 5
tmux new-window -t arlo -n model "bash -c '$S && ros2 run robot_state_publisher robot_state_publisher --ros-args --params-file ~/rsp.yaml; exec bash'"
sleep 2
tmux new-window -t arlo -n odom "bash -c '$S && ros2 run rf2o_laser_odometry rf2o_laser_odometry_node --ros-args --params-file ~/rf2o.yaml; exec bash'"
sleep 3
tmux new-window -t arlo -n slam "bash -c '$S && ros2 launch slam_toolbox online_async_launch.py slam_params_file:=$HOME/slam_demo.yaml; exec bash'"
sleep 5
source /opt/ros/humble/setup.bash
if [ -f ~/demo.rviz ]; then rviz2 -d ~/demo.rviz; else rviz2; fi
