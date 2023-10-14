import rospy
import serial
import utm
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Header
from gps_driver.msg import gps_msg

if __name__ == '__main__':
	SENSOR_NAME = 'gps'
	rospy.init_node('gps_node',anonymous = True)
	serial_port = rospy.get_param('~port','/dev/pts/2')
	serial_baud = rospy.get_param('~baudrate',4800)
	sampling_rate = rospy.get_param('~sampling_rate',1.0)

	port = serial.Serial(serial_port, serial_baud, timeout=3.)

	gps_pub = rospy.Publisher('gps_driver_data',gps_msg, queue_size=10)
	
	try:
		while not rospy.is_shutdown():
			line = port.readline()
			if line == '':
				rospy.logwarn("GPS: No data")
			else:
				gps_data_input = None
				line_str = line.decode("utf-8")
				print(line_str)
				if '$GPGGA' in line_str:
					gps_data_input = line_str.split(",")
				else:
					gps_data_input = None
				if gps_data_input is not None:
					if gps_data_input[3]=='N':
						if gps_data_input[2] !='':
							north_south=1
							lat_dec = (float(gps_data_input[2]))/100
							lat_dec = lat_dec + ((float(gps_data_input[2]))-(lat_dec * 100))/60
							lat_dec = north_south*lat_dec
					else:
						if gps_data_input[2] !='':
							north_south=-1
							lat_dec = (float(gps_data_input[2]))/100
							lat_dec = lat_dec + ((float(gps_data_input[2]))-(lat_dec * 100))/60
							lat_dec = north_south*lat_dec
					if gps_data_input[5]=='E':
						if gps_data_input[4] !='':
							east_west=1
							lon_dec = (float(gps_data_input[4]))/100
							lon_dec = lon_dec + (float((gps_data_input[4]))-(lon_dec * 100))/60
							lon_dec = east_west*lon_dec
					else:
						if gps_data_input[4] !='':
							east_west=-1
							lon_dec = (float(gps_data_input[4]))/100
							lon_dec = lon_dec + (float((gps_data_input[4]))-(lon_dec * 100))/60
							lon_dec = east_west*lon_dec
					
					UTM_conv = utm.from_latlon(lat_dec, lon_dec)
					gps_msg_fields = gps_msg()
				
					
					gps_msg_fields.Latitude = lat_dec
					gps_msg_fields.Longitude = lon_dec
					gps_msg_fields.Altitude = gps_data_input[9]
					gps_msg_fields.UTM_northing = UTM_conv[0]
					gps_msg_fields.UTM_easting = UTM_conv[1]
					gps_msg_fields.Zone = UTM_conv[2]
					gps_msg_fields.Letter = UTM_conv[3]
					time = gps_data_input[1]
					time_sec=(float(time[:2])*3600)+(float(time[2:4])*60)+float(time[4:6])
					gps_msg_fields.header.stamp.secs = int(time_sec)
					time_nsec = float(time[6:])*10e9
					gps_msg_fields.header.stamp.nsecs = int(time_nsec)
					gps_msg_fields.header.frame_id = 'GPS1_Frame'
					
					gps_pub.publish(gps_msg_fields)



	except rospy.ROSInterruptException:
		port.close()
	except serial.serialutil.SerialException:
		rospy.loginfo("Shutting down GPS Driver node ...")
'''
import rospy
import serial
from math import sin, pi
import time
import utm
 
from gps_driver.msg import *
from gps_msg.msg import gps_msg
from std_msgs.msg import Header

from std_msgs.msg import Float64
from std_msgs.msg import String



if __name__ == '__main__':
    SENSOR_NAME = "gps_sensor"
    pub= rospy.Publisher("custom_message",custom,queue_size=10)
    rospy.init_node('gps_sensor')
    serial_port = rospy.get_param('~port','/dev/ttyUSB0')
    serial_baud = rospy.get_param('~baudrate',4800)
    sampling_rate = rospy.get_param('~sampling_rate',5.0)
     
    port = serial.Serial(serial_port, serial_baud, timeout=3.)
    rospy.logdebug("Using gps sensor on port "+serial_port+" at "+str(serial_baud))
    #rospy.logdebug("Using latitude = "+str(latitude_deg)+" & atmosphere offset = "+str(offset))
    rospy.logdebug("Initializing sensor with *0100P4\\r\\n ...")
    
    sampling_count = int(round(1/(sampling_rate*0.007913)))
    rospy.sleep(0.2)        
    #line = port.readline()
     
    #latitude = latitude_deg * pi / 180.
    #depth_pub = rospy.Publisher(SENSOR_NAME+'/depth', Float64, queue_size=5)
    #pressure_pub = rospy.Publisher(SENSOR_NAME+'/pressure', Float64, queue_size=5)
    #odom_pub = rospy.Publisher(SENSOR_NAME+'/odom',Odometry, queue_size=5)
    
    rospy.logdebug("Initialization complete")
    
    rospy.loginfo("Publishing longitude and latitutde.")
        
    #odom_msg = Odometry()
    #odom_msg.header.frame_id = "odom"
    #odom_msg.child_frame_id = SENSOR_NAME
    #odom_msg.header.seq=0
    
   
    msg=custom()
    i=1
    try:
        while not rospy.is_shutdown():
            msg.header.seq=i
            line = port.readline()
            line2=line.decode('latin-1')
            #print(line2)
            if line == '':
                rospy.logwarn("DEPTH: No data")
            else:
                if line2.startswith("$GPGGA") :
                    s =line2.split(",")
                    lat = s[2]
                    lon = s[4]
                    lat_dir = s[3]
                    lon_dir = s[5]
                    utc_time = s[1]
                    alt = s[9]
 #print(lat + " lattitude" + lon + "longitude" )
 
 
#decimal degree lat=43.21583333 lon=71.76388889
#utm_data=utm.from_latlon(float(42.203177),float(-71.052450))
#print(utm_data)
#utm_data2=utm.to_latlon(328041,4689484,19,'T')
#print("\n"+str(utm_data2))
                    degrees_lat=int(float(lat)/100)
                    #print("\nDegree lat:"+str(degrees_lat))
                    minutes_lat=float(lat)-(degrees_lat*100)
                    #print("\tminutes lat:"+str(minutes_lat))
                    degrees_lon=int(float(lon)/100)
                    #print("\nDegree lon:"+str(degrees_lon))
                    minutes_lon=float(lon)-(degrees_lon*100)
                    #print("\tminutes lon:"+str(minutes_lon))
                    dd_lat= float(degrees_lat) + float(minutes_lat)/60
                    dd_lon= float(degrees_lon) + float(minutes_lon)/60 
                    if lon_dir == 'W':
                        dd_lon *= -1
                    if lat_dir == 'S':
                        dd_lat *= -1
                    print("\n"+str(dd_lat)+" "+str(dd_lon))
 
                    utm_data3=utm.from_latlon(dd_lat,dd_lon)
                    print(utm_data3)
                    msg.header.stamp=rospy.get_rostime()
                    msg.header.frame_id="GPS_Data"
                    msg.latitude=dd_lat
                    msg.longitude=dd_lon
                    msg.altitude=float(alt)
                    msg.utm_easting=utm_data3[0]
                    msg.utm_northing=utm_data3[1]
                    msg.zone=float(utm_data3[2])
                    msg.letter_field=utm_data3[3]
                    rospy.loginfo(msg)
                    pub.publish(msg)
                    ++i
    except rospy.ROSInterruptException:
        port.close()
    
    except serial.serialutil.SerialException:
        rospy.loginfo("Shutting down gps_sensor node...")
        
'''
