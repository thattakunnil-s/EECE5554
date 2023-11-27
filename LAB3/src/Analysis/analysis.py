#! /usr/bin/env python3

import bagpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

# Load data from a Bag file
bag_file_path = '/home/steffit/Downloads/EECE5554/LAB3/src/Data/Stationary.bag'
bag = bagpy.bagreader(bag_file_path)

# Extract IMU data
imu_data = bag.message_by_topic('/imu')
imu_readings = pd.read_csv(imu_data)

# Adjust time and sensor data to zero baseline
columns_to_adjust = [
    'IMU.angular_velocity.x',
    'IMU.angular_velocity.y',
    'IMU.angular_velocity.z',
    'IMU.linear_acceleration.x',
    'IMU.linear_acceleration.y',
    'IMU.linear_acceleration.z',
    'MagField.magnetic_field.x',
    'MagField.magnetic_field.y',
    'MagField.magnetic_field.z',
]

for column in columns_to_adjust:
    imu_readings[column] = imu_readings[column] - imu_readings[column].min()

# Calculate Euler angles from quaternions
w = imu_readings['IMU.orientation.w'] * (np.pi / 180)
x = imu_readings['IMU.orientation.x'] * (np.pi / 180)
y = imu_readings['IMU.orientation.y'] * (np.pi / 180)
z = imu_readings['IMU.orientation.z'] * (np.pi / 180)

t0 = +2.0 * (w * x + y * z)
t1 = +1.0 - 2.0 * (x * x + y * y)
roll_x = np.degrees(np.arctan2(t0, t1))

t2 = +2.0 * (w * y - z * x)
t2 = np.where(t2 > +1.0, +1.0, t2)
t2 = np.where(t2 < -1.0, -1.0, t2)
pitch_y = np.degrees(np.arcsin(t2))

t3 = +2.0 * (w * z + x * y)
t4 = +1.0 - 2.0 * (y * y + z * z)
yaw_z = np.degrees(np.arctan2(t3, t4))

# Function to determine distribution type
def get_distribution_type(data):
    # Fit the data to different distributions and calculate the best fit
    dist_names = ['norm', 'expon', 'pareto', 'gamma', 'lognorm', 'weibull_min', 'weibull_max']
    best_fit_name = ''
    best_fit_params = {}
    best_kstest = 1e10  # Initialize with a large value

    for dist_name in dist_names:
        dist = getattr(stats, dist_name)
        params = dist.fit(data)
        kstest_result = stats.kstest(data, dist_name, args=params)

        # Check if this distribution is better (smaller KS statistic) than the previous best fit
        if kstest_result[0] < best_kstest:
            best_fit_name = dist_name
            best_fit_params = params
            best_kstest = kstest_result[0]

    return best_fit_name, best_fit_params

# Function to calculate stats, plot, and save
def calculate_stats_and_plot(data, label, axis_label, filename_prefix):
    # Calculate stats
    mean = data.mean()
    median = np.median(data)
    std_dev = data.std()
    
    # Calculate best fit distribution and parameters
    best_fit_name, best_fit_params = get_distribution_type(data)

    # Print statistics
    print(f'{label} Stats:')
    print(f'Mean: {mean}')
    print(f'Median: {median}')
    print(f'Standard Deviation: {std_dev}')
    print(f'Best Fit Distribution: {best_fit_name}')
    print(f'Best Fit Parameters: {best_fit_params}')

    # Create time series plot
    plt.figure(figsize=(12, 6))
    plt.plot(imu_readings['Time'], data, linestyle='-', marker='o', markersize=5, label=label)
    plt.xlabel('Time (Seconds)')
    plt.ylabel(axis_label)
    plt.title(f'Time vs {axis_label}')
    plt.grid(True)
    plt.legend()

    # Create histogram
    plt.figure(figsize=(12, 6))
    plt.hist(data, bins=40, edgecolor='k', color='skyblue')
    plt.xlabel(axis_label)
    plt.ylabel('Frequency')
    plt.title(f'{axis_label} Histogram (Distribution around the Mean)')
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label='Mean')
    plt.legend()
    plt.grid(True)

    # Show plots
    plt.show()

# Gyroscope data
gyroscope_axes = ['X', 'Y', 'Z']
for axis in gyroscope_axes:
    label = f'Gyroscope (Angular Velocity) Axis {axis}'
    axis_label = f'Angular Velocity_{axis} (rad/sec)'
    filename_prefix = 'Gyroscope'
    data = imu_readings[f'IMU.angular_velocity.{axis.lower()}']
    calculate_stats_and_plot(data, label, axis_label, filename_prefix)

# Accelerometer data
accelerometer_axes = ['X', 'Y', 'Z']
for axis in accelerometer_axes:
    label = f'Accelerometer Axis {axis}'
    axis_label = f'Linear Acceleration_{axis} (m/s²)'
    filename_prefix = 'Accelerometer'
    data = imu_readings[f'IMU.linear_acceleration.{axis.lower()}']
    calculate_stats_and_plot(data, label, axis_label, filename_prefix)

# Magnetometer data
magnetometer_axes = ['X', 'Y', 'Z']
for axis in magnetometer_axes:
    label = f'Magnetometer Axis {axis}'
    axis_label = f'Magnetic Field_{axis} (Gauss)'
    filename_prefix = 'Magnetometer'
    data = imu_readings[f'MagField.magnetic_field.{axis.lower()}']
    calculate_stats_and_plot(data, label, axis_label, filename_prefix)

# Euler angles
euler_angles = [('Roll_X', roll_x), ('Pitch_Y', pitch_y), ('Yaw_Z', yaw_z)]
for label, data in euler_angles:
    axis_label = f'{label} (degrees)'
    filename_prefix = 'EulerAngles'
    calculate_stats_and_plot(data, label, axis_label, filename_prefix)

