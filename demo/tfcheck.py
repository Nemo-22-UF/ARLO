import rclpy, time
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

rclpy.init()
n = Node('tfcheck')
d = {}

def now():
    return n.get_clock().now().nanoseconds / 1e9

def cb(m):
    for t in m.transforms:
        s = t.header.stamp.sec + t.header.stamp.nanosec / 1e9
        d.setdefault(t.header.frame_id + '->' + t.child_frame_id, []).append(s - now())

def scb(m):
    s = m.header.stamp.sec + m.header.stamp.nanosec / 1e9
    d.setdefault('scan', []).append(s - now())

def vcb(m):
    d.setdefault('cmd_vel', []).append(m.linear.x)

n.create_subscription(TFMessage, '/tf', cb, 100)
n.create_subscription(LaserScan, '/scan', scb, qos_profile_sensor_data)
n.create_subscription(Twist, '/cmd_vel', vcb, 10)
end = time.time() + 8
while time.time() < end:
    rclpy.spin_once(n, timeout_sec=0.1)
for k, v in d.items():
    print(k, 'n=%d' % len(v), 'min %.3f max %.3f' % (min(v), max(v)))
