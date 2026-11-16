#!/bin/bash
tmux kill-session -t arlo 2>/dev/null
for p in rviz2 nav2 foxglove slam_toolbox rf2o rplidar robot_state_publisher; do pkill -f $p 2>/dev/null; done
sleep 3
for p in nav2 foxglove slam_toolbox rf2o rplidar robot_state_publisher; do pkill -9 -f $p 2>/dev/null; done
sleep 1
