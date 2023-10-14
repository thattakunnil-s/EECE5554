#!/usr/bin/env python

import rosbag
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import sys
from numpy.polynomial.polynomial import polyfit
from haversine import haversine, Unit


path = sys.argv[1]
fit_line = sys.argv[2]
bag = rosbag.Bag('/home/steffit/Downloads/EECE5554/LAB1/src/Data/'+path+'.bag')

easting, northing = [], []
altitude, time = [], []
latitude, longitude = [], []
hdop = []
for topic, msg, t in bag.read_messages(topics=['/gps']):
    easting.append(msg.UTM_easting)
    northing.append(msg.UTM_northing)
    altitude.append(msg.Altitude)
    latitude.append(msg.Latitude)
    longitude.append(-msg.Longitude)
    hdop.append(msg.HDOP)
    
print('HDOP: ', np.mean(np.array(hdop)))

# Scatterplot of Northing vs Easting
easting, northing = np.array(easting), np.array(northing)
easting -= easting[0]
northing -= northing[0]
if fit_line == 'True':
	b, m = polyfit(easting, northing, 1)
	best_fit = b + m * easting
	mean_error = np.mean(np.abs(northing - best_fit))
	mean_squared_error = np.mean((northing - best_fit)**2)
	print('Mean error: {:.3f}, Mean Squared Error: {:.3f}'.format(mean_error, mean_squared_error))
	plt.plot(easting, best_fit, '-', color='red', label='Best Fit Line')

plt.scatter(easting, northing, s=10)
plt.title(path+" Northing vs Easting Data ")
plt.xlabel("easting")
plt.ylabel("northing")
plt.legend()
plt.tight_layout()
plt.show()

# Altitude vs Time
altitude = np.array(altitude)
#plt.scatter(np.arange(altitude.size), altitude)
plt.scatter(np.arange(altitude.size), altitude, c=np.arange(altitude.size), cmap='viridis')
plt.colorbar(label='time')
plt.title(path+" Altitude vs Time Data ")
plt.xlabel("time")
plt.ylabel("altitude")
plt.tight_layout()
plt.show()

# Histogram of Error
latitude, longitude = np.array(latitude), np.array(longitude)
known_position = (42.336944, 71.09)
known_position_open = (42.338008, 71.092253)
errors = []

def compute_haversine():
	s_lat = latitude*np.pi/180.0
	s_lng = np.deg2rad(longitude)
	e_lat = np.deg2rad(known_latitude)
	e_lng = np.deg2rad(known_longitude)
	d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2
	errors = 2 * 6373 * np.arcsin(np.sqrt(d))
	
for test_position in zip(latitude, longitude):
	errors.append(haversine(test_position, known_position))
	
mean_error = np.mean(errors)
print('Mean Distance: ', mean_error)
plt.hist(errors, bins=20, color='green', edgecolor='black', alpha=0.7)
plt.title(path+" Histogram of Errors")
plt.xlabel("error")
plt.ylabel("frequency")
plt.tight_layout()
plt.show()

bag.close()
