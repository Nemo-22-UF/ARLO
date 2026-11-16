# ARLO

ROS 2 software for the Arlo differential-drive robot in the SmartSystems lab: LiDAR, laser odometry, SLAM mapping, Nav2 navigation, and motor control through the Kria KV260 FPGA.

Maintainer: Nemrod Contreras. Last updated: November 16, 2026.

## Hardware

| Part | Detail |
|---|---|
| Computer | AMD Kria KV260, Ubuntu 22.04, ROS 2 Humble (the bottom board on the robot) |
| LiDAR | RPLidar A1 on `/dev/ttyUSB0` |
| Motors | Driven by PWM from the FPGA overlay `/home/ubuntu/arlo/kv260_v4.bit`, loaded with PYNQ |
| Encoders | Wired to the FPGA but not counting reliably. Not used. |

## Status

| Feature | State |
|---|---|
| LiDAR scan (`/scan`, about 7 Hz) | Working |
| Laser odometry (rf2o, `/odom`) | Working |
| SLAM mapping (slam_toolbox) | Working |
| Motor control from `/cmd_vel` | Working |
| Keyboard driving while mapping | Working, tested on the floor |
| Map view and goal clicking from a laptop (Foxglove) | Working |
| Nav2 starts, accepts goals, plans | Working |
| Nav2 driving the robot to a goal | Set up, **not yet tested on the floor** |
| Wheel encoder odometry | Not working (hardware) |

## Quick start

On the Kria (SSH or its own keyboard):

```bash
~/start_arlo.sh
```

It asks for the password once, starts everything, and after about two minutes prints `motors: OK` and `navigation: active [3]`.

Then connect Foxglove on a laptop to `ws://<kria-ip>:8765`.

To stop:

```bash
~/stop_arlo.sh
sudo pkill -f arlo_motor.py
```

The full step-by-step procedure is in [docs/RUN_GUIDE.md](docs/RUN_GUIDE.md).

## Repository layout

| Path | Contents |
|---|---|
| `demo/start_arlo.sh` | Starts the whole robot in a tmux session named `arlo` |
| `demo/stop_arlo.sh` | Stops every ROS process started by the start script |
| `demo/arlo_motor.py` | Motor controller: `/cmd_vel` to FPGA PWM, with a 0.5 s safety timeout |
| `demo/nav2_arlo.yaml` | Nav2 parameters tuned for Arlo and the Kria |
| `demo/nav_arlo_launch.py` | Nav2 launch file with the lifecycle watchdog disabled |
| `demo/slam_demo.yaml` | slam_toolbox parameters |
| `demo/rf2o.yaml` | Laser odometry parameters |
| `demo/rsp.yaml` | Robot model for robot_state_publisher |
| `demo/fastdds_udp.xml` | DDS profile that lets the root motor node talk to user nodes |
| `demo/goal_ahead.py` | Sends a Nav2 goal a given distance straight ahead |
| `demo/tfcheck.py` | Diagnostic: prints how stale each transform is |
| `demo/start_demo.sh` | Older script: LiDAR, odometry, SLAM, and RViz only |
| `arlobot_ws/src/arlobot` | Original robot package from the previous student, with fixes |
| `docs/RUN_GUIDE.md` | How to run the demo |

On the Kria, the files in `demo/` live in `/home/ubuntu/`.

## Dependencies on the Kria

- ROS 2 Humble with `nav2_bringup`, `slam_toolbox`, `rplidar_ros`, `teleop_twist_keyboard`, `foxglove_bridge`
- `rf2o_laser_odometry` built in `~/arlobot_ws`
- PYNQ (`/etc/profile.d/pynq_venv.sh`) for the FPGA overlay
- `tmux`

## Things learned the hard way

1. **Use `arlo_motor.py`, not `test_motor_controller`.** The old controller closes its loop on the encoders. With the encoders reading zero it pushes the motors toward full power.
2. **The motor node must run as root** (PYNQ needs it), and root and user nodes cannot share Fast DDS shared memory. `fastdds_udp.xml` forces the motor node onto UDP so `/cmd_vel` reaches it.
3. **Do not run RViz or the desktop on the Kria together with SLAM and Nav2.** The board overloads, SLAM's transform goes stale for seconds, and Nav2 stops. The start script stops the desktop (`gdm`) and Ubuntu's background updates. View the robot from a laptop with Foxglove.
4. **rf2o publishes its transform 0.25 to 0.45 s after each scan.** SLAM (`transform_timeout: 0.8`) and Nav2 (`transform_tolerance: 1.0`) are set to wait for it. With the defaults, scans get dropped.
5. **If the Kria does not boot** (fan on, no network), unplug the USB-to-UART cable and power-cycle. A cable attached at power-on can interrupt the boot.
6. The driver's `frame_id` must be `rplidar` to match the URDF.

## Next steps

- Test and tune Nav2 goal driving on an open floor
- Calibrate the speed mapping in `arlo_motor.py` (`US_PER_MPS`, `FWD_MIN_US`)
- Fix the encoder wiring or power so wheel odometry can be fused with laser odometry
- Record a demonstration video
