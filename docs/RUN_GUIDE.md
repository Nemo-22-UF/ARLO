# ARLO demo: run guide

For whoever runs the robot. No ROS knowledge needed. Written by Nemrod Contreras, November 16, 2026.

## What the demo shows

The robot scans the room with its LiDAR and builds a map live while it drives. The map, the laser points, and the robot's position appear on a laptop.

| Part | State |
|---|---|
| **A. Drive with the keyboard while the map builds** | Proven. Use this as the main demo. |
| **B. Click a goal and the robot drives there by itself** | Set up, but not yet tested on the floor. Try it only after testing it in the room first. |

## Before the day

1. **Foxglove** installed on the demo laptop (foxglove.dev/download, free account).
2. **Access to the Kria.** Nemrod shares the machine `kria` through Tailscale. Its address is `100.80.54.31`. Without Tailscale, the laptop and the Kria must be on the same network and you use the Kria's local IP instead.
3. **The password** for the `ubuntu` user. Ask Nemrod.
4. **Check the network in the demo room.** The Kria connects by WiFi. If it cannot get online there, SSH and Foxglove will not reach it. Test this ahead of time.
5. **Power.** The Kria runs from its wall adapter. Bring a long extension cord. The cord limits how far the robot can drive, so hold it clear of the wheels.

## 1. Power on

1. Plug in the Kria (the **bottom** board). Turn on the **motor power switch**.
2. Wait about 2 minutes for it to boot.
3. If it does not come up (fan runs, but no network): unplug the USB-to-UART cable from the board, then unplug and replug the power.

## 2. Start the robot

On the laptop, open a terminal:

```bash
ssh ubuntu@100.80.54.31
```

Then:

```bash
~/start_arlo.sh
```

Enter the password when it asks. After about 2 minutes it should print:

```
motors: OK
navigation: active [3]
Done. Connect Foxglove to ws://100.80.54.31:8765
```

If the Kria's own monitor shows a black screen with text, that is intended. The script turns the desktop off to save processing power.

## 3. Open the map view

1. Open Foxglove, choose **Open connection**, then **Foxglove WebSocket**.
2. Enter `ws://100.80.54.31:8765` and click **Open**.
3. Use a **3D panel** with these settings:
   - Display frame: `map`
   - Topics switched on: `/map`, `/scan`, `/local_costmap/costmap`, `/plan`
   - `/scan`: Color mode `Flat`, a bright color, Point size `4`
   - Publish section, **2D pose** topic: `/goal_pose`

What you see: black is walls and obstacles, white is free floor, grey is unexplored, and the colored points are the live laser scan.

## 4. Demo A: drive with the keyboard

In the SSH terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.15 -p turn:=0.6
```

Click on that terminal, then **hold** a key to drive:

| Key | Action |
|---|---|
| `i` | forward |
| `,` | backward |
| `j` | turn left |
| `l` | turn right |
| `k` | stop |

Releasing the key stops the robot within half a second. Drive slowly around the area and the map fills in on the laptop. Press `Ctrl+C` to quit.

## 5. Demo B: drive to a goal by itself (test first)

Only with at least half a meter of free space around the robot.

**From Foxglove:** click the publish tool in the 3D panel (target icon), choose **Publish 2D pose**, click on free (white) floor, drag in the direction the robot should face, and release. A path appears and the robot follows it.

**Or from the terminal,** to drive a set distance straight ahead (here 1 meter):

```bash
python3 ~/goal_ahead.py 1.0
```

Keep a hand near the motor power switch the first times.

## 6. Stop and shut down

```bash
~/stop_arlo.sh
sudo pkill -f arlo_motor.py
sudo shutdown now
```

Wait for the lights to settle, then unplug.

## If something goes wrong

| Problem | What to do |
|---|---|
| Robot does anything unexpected | Flip the motor power switch. |
| `motors: NOT READY` | Run `cat ~/motor.log` to see the error, then run `~/start_arlo.sh` again. |
| Keys pressed but the robot does not move | Check the motor power switch. Check `tail ~/motor.log` shows `L ... R ...` lines while you hold a key. |
| Map is frozen or the robot jumps around on it | Run `~/start_arlo.sh` again. It restarts everything cleanly. |
| Foxglove cannot connect | Check the laptop can reach the Kria (`ping 100.80.54.31`). Check Tailscale is on and signed in. |
| A goal is sent but the robot stays still | The robot or the goal is too close to an obstacle. Move it to open floor and try a goal on white space. |
| Everything is slow | Make sure nothing else is open on the Kria. Do not start RViz or the desktop there. |
| Need to look at a part's log | `tmux attach -t arlo`, switch windows with `Ctrl+b` then a number, leave with `Ctrl+b` then `d`. |

## Good to know

- The start script is safe to run again at any time.
- The motor controller stops the wheels if it receives no command for half a second.
- The wheel encoders are not used. Position comes from the LiDAR.
- People standing close to the robot appear as obstacles on the map.
