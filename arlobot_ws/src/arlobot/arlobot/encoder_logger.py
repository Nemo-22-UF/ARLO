#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

from pynq import Overlay
import time

# === Load FPGA Overlay ===
overlay = Overlay("/home/ubuntu/overlays/arlobot_pwm_encoder/your_overlay.bit")
encoder_left = overlay.encoder_decoder_left_0  # Change these names if needed
encoder_right = overlay.encoder_decoder_right_0

class EncoderLogger(Node):
    def __init__(self):
        super().__init__('encoder_logger')
        self.left_pub = self.create_publisher(Int32, 'left_ticks', 10)
        self.right_pub = self.create_publisher(Int32, 'right_ticks', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info("Encoder Logger Node Started")

    def timer_callback(self):
        left_ticks = encoder_left.read(0x00)  # Adjust offset if needed
        right_ticks = encoder_right.read(0x00)

        left_msg = Int32()
        left_msg.data = left_ticks
        self.left_pub.publish(left_msg)

        right_msg = Int32()
        right_msg.data = right_ticks
        self.right_pub.publish(right_msg)

        self.get_logger().info(f"Encoders - L: {left_ticks} R: {right_ticks}")

def main(args=None):
    rclpy.init(args=args)
    node = EncoderLogger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
