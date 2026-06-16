#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from pynq import Overlay

# === Robot Parameters ===
WHEEL_BASE = 0.3937  # meters
MAX_PWM = 100.0
MAX_SPEED = 0.3

# === Load FPGA Overlay ===
overlay = Overlay("/home/ubuntu/overlays/arlobot_pwm_encoder/your_overlay.bit")
pwm_ip = overlay.motor_pwm_0  # Adjust name if different

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        self.get_logger().info("Motor Controller Node Started")

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        left_speed = linear - (angular * WHEEL_BASE / 2)
        right_speed = linear + (angular * WHEEL_BASE / 2)

        left_pwm = max(min((left_speed / MAX_SPEED) * MAX_PWM, MAX_PWM), -MAX_PWM)
        right_pwm = max(min((right_speed / MAX_SPEED) * MAX_PWM, MAX_PWM), -MAX_PWM)

        # Send to motor IP - update addresses if needed
        pwm_ip.write(0x00, int(left_pwm))
        pwm_ip.write(0x04, int(right_pwm))

        self.get_logger().info(f"PWM L: {int(left_pwm)}  R: {int(right_pwm)}")

def main(args=None):
    rclpy.init(args=args)
    node = MotorController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
