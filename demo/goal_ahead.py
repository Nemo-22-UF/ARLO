import sys, math, time, rclpy
from rclpy.node import Node
from rclpy.time import Time
from geometry_msgs.msg import PoseStamped
from tf2_ros import Buffer, TransformListener

d = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
rclpy.init()
n = Node('goal_ahead')
buf = Buffer()
TransformListener(buf, n)
pub = n.create_publisher(PoseStamped, '/goal_pose', 10)
t = None
end = time.time() + 20
while time.time() < end and (t is None or pub.get_subscription_count() == 0):
    rclpy.spin_once(n, timeout_sec=0.2)
    try:
        t = buf.lookup_transform('map', 'base_link', Time())
    except Exception:
        pass
if t is None or pub.get_subscription_count() == 0:
    print('not ready: no robot position or Nav2 not listening')
    sys.exit(1)
q = t.transform.rotation
yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
g = PoseStamped()
g.header.frame_id = 'map'
g.header.stamp = n.get_clock().now().to_msg()
g.pose.position.x = t.transform.translation.x + d * math.cos(yaw)
g.pose.position.y = t.transform.translation.y + d * math.sin(yaw)
g.pose.orientation = q
pub.publish(g)
for _ in range(5):
    rclpy.spin_once(n, timeout_sec=0.2)
print('goal sent %.2f m ahead' % d)
