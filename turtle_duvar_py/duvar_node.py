#!/usr/bin/env python3
"""Duvardan kacan kaplumbaga."""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
try:
    from turtlesim_msgs.msg import Pose
except ImportError:
    from turtlesim.msg import Pose


class DuvarNode(Node):
    def __init__(self):
        super().__init__('duvar_node')

        # Bonus: hiz ve sinirlar parametre
        self.declare_parameter('linear_speed', 1.5)
        self.declare_parameter('angular_speed', 2.0)
        self.declare_parameter('min_limit', 1.0)
        self.declare_parameter('max_limit', 10.0)

        self.pose = None

        # Abone
        self.sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)
        # Yayinci
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.control_timer = self.create_timer(0.1, self.control_loop)
        self.log_timer = self.create_timer(1.0, self.log_position)
        self.get_logger().info('duvar_node basladi.')

    def pose_callback(self, msg):
        self.pose = msg

    def control_loop(self):
        if self.pose is None:
            return

        lin = self.get_parameter('linear_speed').value
        ang = self.get_parameter('angular_speed').value
        lo = self.get_parameter('min_limit').value
        hi = self.get_parameter('max_limit').value

        x, y = self.pose.x, self.pose.y
        cmd = Twist()

        if x < lo or x > hi or y < lo or y > hi:
            cmd.linear.x = lin * 0.5
            cmd.angular.z = ang
        else:
            cmd.linear.x = lin
            cmd.angular.z = 0.0

        self.pub.publish(cmd)

    def log_position(self):
        if self.pose is None:
            self.get_logger().warn('Henuz pose verisi gelmedi.')
            return
        self.get_logger().info(
            f'Konum -> x: {self.pose.x:.2f}, y: {self.pose.y:.2f}, '
            f'theta: {self.pose.theta:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = DuvarNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
