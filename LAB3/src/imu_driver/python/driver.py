#!/usr/bin/env python3

import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Imu, MagneticField
from imu_driver.msg import imu_msg
from imu_driver.srv import convert_to_quaternion
import serial
import sys

def append_checksum(nmea_command):
    checksum = 0
    for char in nmea_command:
        checksum ^= ord(char)
    return f"${nmea_command}*{checksum:02X}\r\n"

def configure_imu(serial_connection):
    configure_command_40hz = append_checksum("VNWRG,07,40")
    serial_connection.write(configure_command_40hz.encode())
    divisor = int(800 / 40)  
    configure_output_message = append_checksum(f"VNWRG,75,2,{divisor},01,0029")
    serial_connection.write(configure_output_message.encode())

def euler_to_quaternion(roll, pitch, yaw):
    rospy.wait_for_service('convert_to_quaternion')
    try:
        convert_service = rospy.ServiceProxy('convert_to_quaternion', convert_to_quaternion)
        resp = convert_service(roll, pitch, yaw)
        return resp.x, resp.y, resp.z, resp.w
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

def read_imu_data(serial_port):
    imu_publisher = rospy.Publisher('imu', imu_msg, queue_size=10)
    rospy.init_node('imu_data_reader', anonymous=True)
    serial_connection = serial.Serial(serial_port, 115200)
    configure_imu(serial_connection)
    
    while not rospy.is_shutdown():
        raw_data = serial_connection.readline().decode('utf-8')
        data_elements = raw_data.split(',')
        
        if '$VNYMR' in data_elements[0]:
            orientation_yaw = float(data_elements[1])
            orientation_pitch = float(data_elements[2])
            orientation_roll = float(data_elements[3])
            
            imu_data = imu_msg()
            header = Header()
            header.stamp = rospy.Time.now()
            header.frame_id = "IMU1_Frame"
            imu_data.Header = header
            
            imu_data.MagField.magnetic_field.x = float(data_elements[4]) * 0.0001
            imu_data.MagField.magnetic_field.y = float(data_elements[5]) * 0.0001
            imu_data.MagField.magnetic_field.z = float(data_elements[6]) * 0.0001

            imu_data.IMU.linear_acceleration.x = float(data_elements[7])
            imu_data.IMU.linear_acceleration.y = float(data_elements[8])
            imu_data.IMU.linear_acceleration.z = float(data_elements[9])

            imu_data.IMU.angular_velocity.x = float(data_elements[10])
            imu_data.IMU.angular_velocity.y = float(data_elements[11])
            imu_data.IMU.angular_velocity.z = float(data_elements[12].split('*')[0])

            imu_data.IMU_backup = raw_data

            quaternion = euler_to_quaternion(orientation_roll, orientation_pitch, orientation_yaw)
            imu_data.IMU.orientation.x = quaternion[0]
            imu_data.IMU.orientation.y = quaternion[1]
            imu_data.IMU.orientation.z = quaternion[2]
            imu_data.IMU.orientation.w = quaternion[3]
            
            rospy.loginfo(imu_data)
            imu_publisher.publish(imu_data)

if __name__ == '__main__':
    try:
        serial_port_param = rospy.get_param('~port')
        read_imu_data(serial_port_param)
    except rospy.ROSInterruptException:
        pass

