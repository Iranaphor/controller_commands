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
        self.prior = Joy()
        self.prior.buttons = [0]*16
        self.joy_sub = self.create_subscription(Joy, '/joy', self.joy_cb, 10)

        # Load params config
        if not self.has_parameter('action_modifier'):
            self.declare_parameter('action_modifier', int(4))
        self.modifier_control = self.get_parameter('action_modifier').value
        self.modifier = ''

        for k in ['', '_alt']:
            for j in ['press', 'release']:
                for i in range(0,15):
                    if not self.has_parameter(f'{j}{k}.{i}'):
                        self.declare_parameter(f'{j}{k}.{i}', str(''))
        #self.declare_parameter('press_alt')
        #self.declare_parameter('release')
        #self.declare_parameter('release_alt')
        #self.declare_parameter('release_alt')


    ##############################
    ### Joy Controller Spawning
    def joy_cb(self, msg):

        for b in range(0,len(msg.buttons)):

            # Switch to L1 alternative bindings
            if msg.buttons[self.modifier_control] and not self.prior.buttons[self.modifier_control]:
                self.modifier = '_alt'
            if not msg.buttons[self.modifier_control] and self.prior.buttons[self.modifier_control]:
                self.modifier = ''

            # Execute associated command
            if msg.buttons[b] and not self.prior.buttons[b]:
                cmd = self.get_parameter(f'press{self.modifier}.{b}').value
                self.get_logger().info(f'🎮  | button {b}{self.modifier} pressed:  performing cmd: {cmd}')
                subprocess.run(cmd, shell=True)

            if not msg.buttons[b] and self.prior.buttons[b]:
                cmd = self.get_parameter(f'release{self.modifier}.{b}').value
                self.get_logger().info(f'🎮  | button {b}{self.modifier} released: performing cmd: {cmd}')
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
