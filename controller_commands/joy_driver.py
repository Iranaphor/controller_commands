# -*- coding: utf-8 -*-
#! /usr/bin/env python3
# ----------------------------------
# @author: jheselden
# @email: jheselden@lincoln.ac.uk
# @date:
# ----------------------------------


import yaml
import subprocess

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy
from rclpy.parameter import Parameter

from ament_index_python.packages import get_package_share_directory

from sensor_msgs.msg import Joy


class JoyDriver(Node):

    def __init__(self):

        super().__init__('joy_driver')
        self.get_logger().info('🎮 | Joy Driver')

        # Set rosparams if they are not already set
        self.get_logger().info('🎮 | ROS params declared\n')

        # Check for joy trigger
        self.reset_button = 5
        self.spawn_button = 8
        self.prior = Joy()
        self.prior.buttons = [0]*16
        self.joy_sub = self.create_subscription(Joy, '/joy', self.joy_cb, 10)

        # Load config
        PKG = get_package_share_directory('controller_commands')
        params_file = f'{PKG}/config/conf.yaml'
        with open(params_file) as f:
            self.actions = yaml.load(f)
        print(self.actions)


    ##############################
    ### Joy Controller Spawning
    def joy_cb(self, msg):

        for b in range(0,len(msg.buttons)):

            if msg.buttons[b] and not self.prior.buttons[b]:
                cmd = self.actions[b]['press']
                self.get_logger().info(f'🎮  | button {b} pressed:  performing cmd: {cmd}')
                subprocess.run(cmd, shell=True)

            if not msg.buttons[b] and self.prior.buttons[b]:
                cmd = self.actions[b]['release']
                self.get_logger().info(f'🎮  | button {b} released: performing cmd: {cmd}')
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
