#! /usr/bin/env python3

import rospy
import serial
import utm
import math
from std_msgs.msg import Header
from gps_driver.msg import gps_msg

port1 = rospy.get_param('driver/port')

def read(port):
  publisher = rospy.Publisher('gps', gps_msg, queue_size=10)
  rospy.init_node('gps_data')
  port = serial.Serial(port, 4800)
  while not rospy.is_shutdown():
     data = port.readline()
     data_str = data.decode('utf-8')
     print(data_str)
     #if data == '':
	#rospy.logwarn("GPS: No data")
     data_split = data_str.split(',')
     if '$GPGGA' in data_split[0]:
     
        time_str = data_split[1]
        hours = int(time_str[:2])
        minutes = int(time_str[2:4])
        seconds = int(time_str[4:6])
        milliseconds = int(time_str.split('.')[1])

        time_stamp_sec = hours * 3600 + minutes * 60 + seconds
        time_stamp_nsec = milliseconds * 1000000

        lat = float(data_split[2])
        lat_direction = data_split[3]
        latitude = math.trunc(lat//100) + (lat%100)/60
        
        long = float(data_split[4])
        long_direction = data_split[5]
        longitude = math.trunc(long//100) + (long%100)/60
        
        altitude = float(data_split[9])
        hdop = float(data_split[8])
        
        if lat_direction == 'S':
           latitude *= -1
        if long_direction == 'W':
           longitude *= -1
           
        msg = gps_msg()
        msg.Header = Header()
        msg.Header.frame_id = "GPS1_Frame"
        msg.Header.stamp.secs = time_stamp_sec  
        msg.Header.stamp.nsecs = time_stamp_nsec 
        msg.Latitude = latitude
        msg.Longitude = longitude
        msg.Altitude = altitude
        msg.HDOP = hdop
        msg.UTM_easting, msg.UTM_northing, msg.Zone, msg.Letter = utm.from_latlon(latitude, longitude)
        publisher.publish(msg)

if __name__ == '__main__':
  try:
     read(port1)
  except rospy.ROSInterruptException:
     pass
