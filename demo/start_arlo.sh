#!/bin/bash
S="source /opt/ros/humble/setup.bash && source ~/arlobot_ws/install/setup.bash"
echo "[1/4] password (needed for the motors)"
sudo -v || exit 1
sudo systemctl stop gdm apt-daily.timer apt-daily-upgrade.timer unattended-upgrades 2>/dev/null
sudo swapon /swapfile 2>/dev/null
sudo pkill -f arlo_motor.py 2>/dev/null
~/stop_arlo.sh
echo "[2/4] motors"
sudo bash -c 'source /etc/profile.d/pynq_venv.sh; source /opt/ros/humble/setup.bash; export FASTRTPS_DEFAULT_PROFILES_FILE=/home/ubuntu/fastdds_udp.xml; nohup python3 /home/ubuntu/arlo_motor.py > /home/ubuntu/motor.log 2>&1 &'
echo "[3/4] lidar, odometry, mapping"
tmux new-session -d -s arlo -n lidar "bash -c '$S && ros2 launch rplidar_ros rplidar_a1_launch.py serial_port:=/dev/ttyUSB0 frame_id:=rplidar; exec bash'"
sleep 5
tmux new-window -t arlo -n model "bash -c '$S && ros2 run robot_state_publisher robot_state_publisher --ros-args --params-file ~/rsp.yaml; exec bash'"
sleep 2
tmux new-window -t arlo -n odom "bash -c '$S && ros2 run rf2o_laser_odometry rf2o_laser_odometry_node --ros-args --params-file ~/rf2o.yaml; exec bash'"
sleep 3
tmux new-window -t arlo -n slam "bash -c '$S && ros2 launch slam_toolbox online_async_launch.py slam_params_file:=$HOME/slam_demo.yaml; exec bash'"
sleep 8
echo "[4/4] navigation and laptop bridge"
tmux new-window -t arlo -n nav2 "bash -c '$S && ros2 launch ~/nav_arlo_launch.py params_file:=$HOME/nav2_arlo.yaml use_sim_time:=false; exec bash'"
tmux new-window -t arlo -n fox "bash -c '$S && ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765; exec bash'"
echo "waiting 75 s for navigation to start..."
sleep 75
grep -q "arlo_motor ready" ~/motor.log && echo "motors: OK" || echo "motors: NOT READY (see ~/motor.log)"
source /opt/ros/humble/setup.bash
echo "navigation: $(ros2 lifecycle get /bt_navigator 2>&1)"
echo "Done. Connect Foxglove to ws://100.80.54.31:8765"
