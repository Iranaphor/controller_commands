# -*- coding: utf-8 -*-
#! /usr/bin/env python3
# ----------------------------------
# @author: jheselden
# @email: jheselden@lincoln.ac.uk
# @date:
# ----------------------------------

import subprocess

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy
from rclpy.parameter import Parameter

from sensor_msgs.msg import Joy


class JoyDriver(Node):

    def __init__(self):

        super().__init__('joy_driver')
        self.get_logger().info('🎮 | Joy Driver')

        # Set rosparams if they are not already set
        self.get_logger().info('🎮 | ROS params declared')

        # Check for joy trigger
        self.reset_button = 5
        self.spawn_button = 8
        self.prior = Joy()
        self.prior.buttons = [0]*16
        self.joy_sub = self.create_subscription(Joy, '/joy', self.joy_cb, 10)

        # Define actions to run
        self.actions = {
            'press':{
                0: 'touch ~/Desktop/x0.md',
                1: 'touch ~/Desktop/x1.md',
                2: 'touch ~/Desktop/x2.md',
                3: 'touch ~/Desktop/x3.md',
                4: 'touch ~/Desktop/x4.md',
                5: 'touch ~/Desktop/x5.md',
                6: 'touch ~/Desktop/x6.md',
                7: 'touch ~/Desktop/x7.md',
                8: 'touch ~/Desktop/x8.md',
                9: 'touch ~/Desktop/x9.md',
                10: 'touch ~/Desktop/x10.md',
                11: 'touch ~/Desktop/x11.md',
                12: 'touch ~/Desktop/x12.md',
                13: 'touch ~/Desktop/x13.md',
                14: 'touch ~/Desktop/x14.md',
                15: 'touch ~/Desktop/x15.md'
            },
            'release': {
                0: 'rm ~/Desktop/x0.md',
                1: 'rm ~/Desktop/x1.md',
                2: 'rm ~/Desktop/x2.md',
                3: 'rm ~/Desktop/x3.md',
                4: 'rm ~/Desktop/x4.md',
                5: 'rm ~/Desktop/x5.md',
                6: 'rm ~/Desktop/x6.md',
                7: 'rm ~/Desktop/x7.md',
                8: 'rm ~/Desktop/x8.md',
                9: 'rm ~/Desktop/x9.md',
                10: 'rm ~/Desktop/x10.md',
                11: 'rm ~/Desktop/x11.md',
                12: 'rm ~/Desktop/x12.md',
                13: 'rm ~/Desktop/x13.md',
                14: 'rm ~/Desktop/x14.md',
                15: 'rm ~/Desktop/x15.md'
            }
        }

    ##############################
    ### Joy Controller Spawning
    def joy_cb(self, msg):

        for b in range(1,len(msg.buttons)):

            if msg.buttons[b] and not self.prior.buttons[b]:
                self.get_logger().info(f'🎮  | button {b} pressed')
                cmd = self.actions['press'][b]
                self.get_logger().info(f'🎮  | performing cmd: {cmd}')
                subprocess.run(cmd, shell=True)

            if not msg.buttons[b] and self.prior.buttons[b]:
                self.get_logger().info(f'🎮  | button {b} un-pressed')
                cmd = self.actions['release'][b]
                self.get_logger().info(f'🎮  | performing cmd: {cmd}')
                subprocess.run(cmd, shell=True)

        self.prior = msg


def main(args=None):
    rclpy.init(args=args)

    JD = JoyDriver()
    try:
        rclpy.spin(JD)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
