#!/usr/bin/env python3
import sys
sys.path.insert(0, "/usr/local/share/pynq-venv/lib/python3.10/site-packages")
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pynq import Overlay

WHEEL_BASE = 0.3875
MAX_WHEEL_SPEED = 0.30
STOP_US = 1500
FWD_MIN_US = 1525
REV_MIN_US = 1475
US_PER_MPS = 320.0
DEADBAND = 0.01
TIMEOUT_S = 0.5


class Motor(Node):
    def __init__(self):
        super().__init__('arlo_motor')
        self.pwm = Overlay('/home/ubuntu/arlo/kv260_v4.bit').motor_pwm_0
        self.last = 0.0
        self.moving = False
        self.stop()
        self.create_subscription(Twist, '/cmd_vel', self.cb, 10)
        self.create_timer(0.1, self.watchdog)
        self.get_logger().info('arlo_motor ready')

    def to_us(self, v):
        v = max(-MAX_WHEEL_SPEED, min(MAX_WHEEL_SPEED, v))
        if abs(v) < DEADBAND:
            return STOP_US
        if v > 0:
            return int(FWD_MIN_US + US_PER_MPS * v)
        return int(REV_MIN_US + US_PER_MPS * v)

    def write(self, l, r):
        self.pwm.write(0x00, l)
        self.pwm.write(0x04, r)

    def stop(self):
        self.write(STOP_US, STOP_US)
        self.moving = False

    def cb(self, msg):
        v, w = msg.linear.x, msg.angular.z
        l = self.to_us(v - w * WHEEL_BASE / 2.0)
        r = self.to_us(v + w * WHEEL_BASE / 2.0)
        self.write(l, r)
        self.last = time.time()
        self.moving = (l != STOP_US or r != STOP_US)
        self.get_logger().info(f'L {l} R {r}', throttle_duration_sec=1.0)

    def watchdog(self):
        if self.moving and time.time() - self.last > TIMEOUT_S:
            self.stop()
            self.get_logger().warn('cmd_vel timeout, stopped')


def main():
    rclpy.init()
    node = Motor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
