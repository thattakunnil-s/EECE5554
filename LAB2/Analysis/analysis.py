#!/usr/bin/env python

import rosbag
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from haversine import haversine

def gather_data_from_bag(filepath):
    bag_data = rosbag.Bag(filepath)
    data = {
        'easting': [],
        'northing': [],
        'altitude': [],
        'latitude': [],
        'longitude': [],
        'hdop': []
    }
    
    for topic, msg, _ in bag_data.read_messages(topics=['/gps']):
        data['easting'].append(msg.UTM_easting)
        data['northing'].append(msg.UTM_northing)
        data['altitude'].append(msg.Altitude)
        data['latitude'].append(msg.Latitude)
        data['longitude'].append(-msg.Longitude)
        data['hdop'].append(msg.HDOP)
    
    return data

def display_2d_histogram(easting, northing, title):
    easting -= easting[0]
    northing -= northing[0]
    easting_deviation = easting - np.mean(easting)
    northing_deviation = northing - np.mean(northing)
    mean_error = (np.mean(np.abs(easting_deviation)) + np.mean(np.abs(northing_deviation)))/2
    mse = (np.mean(easting_deviation**2) + np.mean(northing_deviation**2))/2
    std_dev = (np.std(easting) + np.std(northing))/ 2
    print(f"Average Deviation in Easting: {np.mean(np.abs(easting_deviation)):.3f}")
    print(f"Average Deviation in Northing: {np.mean(np.abs(northing_deviation)):.3f}")
    print(f"Mean Error: {mean_error:.3f}")
    print(f"Mean Squared Error: {mse:.3f}")
    print(f"Standard Deviation: {std_dev:.3f}")
    plt.hist2d(easting, northing, bins=50, cmap='viridis', cmin=1, vmax=10)
    plt.colorbar(label='Frequency')
    plt.title(title)
    plt.xlabel("Easting")
    plt.ylabel("Northing")
    plt.tight_layout()
    plt.show()

def enhanced_histogram(errors, title):
    std_dev = np.std(errors)
    plt.hist(errors, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(np.mean(errors), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {np.mean(errors):.2f}')
    plt.axvline(np.mean(errors) + std_dev, color='green', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_dev:.2f}')
    plt.axvline(np.mean(errors) - std_dev, color='green', linestyle='dashed', linewidth=1)
    plt.title(title)
    plt.xlabel("Error")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    filepath = '/home/steffit/Downloads/EECE5554/LAB2/Data/' + sys.argv[1] + '.bag'
    data = gather_data_from_bag(filepath)
    
    print('HDOP:', np.mean(np.array(data['hdop'])))
    
    display_2d_histogram(np.array(data['easting']), np.array(data['northing']), sys.argv[1] + " Northing vs Easting Data")
    
    known_coords = (42.336944, 71.09)
    errors = [haversine(pos, known_coords) for pos in zip(data['latitude'], data['longitude'])]
    print('Mean Distance:', np.mean(errors))
    
    enhanced_histogram(errors, sys.argv[1] + " Histogram of Errors")

if __name__ == "__main__":
    import sys
    main()

'''
import rosbag
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from haversine import haversine

def process_bag_data(filepath):
    bag_data = rosbag.Bag(filepath)
    data = {
        'easting': [],
        'northing': [],
        'altitude': [],
        'latitude': [],
        'longitude': [],
        'hdop': []
    }
    
    for topic, msg, _ in bag_data.read_messages(topics=['/gps']):
        data['easting'].append(msg.UTM_easting)
        data['northing'].append(msg.UTM_northing)
        data['altitude'].append(msg.Altitude)
        data['latitude'].append(msg.Latitude)
        data['longitude'].append(-msg.Longitude)
        data['hdop'].append(msg.HDOP)
    
    return data

def plot_northing_vs_easting(easting, northing, title):
    easting -= easting[0]
    northing -= northing[0]
    
    _, slope = polyfit(easting, northing, 1)
    predicted = easting * slope
    error = np.abs(northing - predicted)
    
    print(f'Mean error: {np.mean(error):.3f}, Mean Squared Error: {np.mean(error**2):.3f}')
    
    plt.scatter(easting, northing, s=10)
    plt.title(title)
    plt.xlabel("Easting")
    plt.ylabel("Northing")
    plt.tight_layout()
    plt.show()

def plot_error_histogram(errors, title):
    plt.hist(errors, bins=20, color='green', edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel("Error")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def main():
    filepath = '/home/steffit/Downloads/EECE5554/LAB2/Data/' + sys.argv[1] + '.bag'
    data = process_bag_data(filepath)
    
    print('HDOP:', np.mean(np.array(data['hdop'])))
    
    plot_northing_vs_easting(np.array(data['easting']), np.array(data['northing']), sys.argv[1] + " Northing vs Easting Data")
    
    known_coords = (42.336944, 71.09)
    errors = [haversine(pos, known_coords) for pos in zip(data['latitude'], data['longitude'])]
    print('Mean Distance:', np.mean(errors))
    
    plot_error_histogram(errors, sys.argv[1] + " Histogram of Errors")

if __name__ == "__main__":
    import sys
    main()
'''
