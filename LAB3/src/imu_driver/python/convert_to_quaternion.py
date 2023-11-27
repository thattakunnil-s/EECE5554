#!/usr/bin/env python3

import rospy
import numpy as np
from imu_driver.srv import convert_to_quaternion, convert_to_quaternionResponse

def handle_convert_to_quaternion(req):
    roll = req.roll * np.pi / 180  # Convert to radians
    pitch = req.pitch * np.pi / 180
    yaw = req.yaw * np.pi / 180

    # Quaternion conversion
    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

    return convert_to_quaternionResponse(x=qx, y=qy, z=qz, w=qw)

def convert_to_quaternion_server():
    rospy.init_node('convert_to_quaternion_server')
    s = rospy.Service('convert_to_quaternion', convert_to_quaternion, handle_convert_to_quaternion)
    print("Convert to quaternion service ready.")
    rospy.spin()

if __name__ == "__main__":
    convert_to_quaternion_server()

