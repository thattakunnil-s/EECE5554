import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from bagpy import bagreader
import scipy.integrate as integrate
from scipy.signal import butter, filtfilt

# Setting up the plot style
sns.set_style("dark")
sns.color_palette("viridis", as_cmap=True)
plt.rcParams.update({'font.size': 10})

# Reading data from bag file
bag = bagreader("/home/steffit/Downloads/EECE5554/LAB4/src/Data/data_driving.bag")
imu_data_path = bag.message_by_topic('/imu')
imu_data = pd.read_csv(imu_data_path)
imu_data = imu_data[10000:101000]

# Hard-Iron Calibration Function
def hard_iron_calibration(data):
    min_x = min(data['MagField.magnetic_field.x'])
    max_x = max(data['MagField.magnetic_field.x'])
    min_y = min(data['MagField.magnetic_field.y'])
    max_y = max(data['MagField.magnetic_field.y'])
    x_offset = (min_x + max_x) / 2.0
    y_offset = (min_y + max_y) / 2.0
    corrected_x = data['MagField.magnetic_field.x'] - x_offset
    corrected_y = data['MagField.magnetic_field.y'] - y_offset
    return corrected_x, corrected_y

mag_x_corr, mag_y_corr = hard_iron_calibration(imu_data)
yaw_raw = np.arctan2(mag_y_corr, mag_x_corr)

# Soft-Iron Calibration Function
def soft_iron_calibration(x_corr, y_corr):
    radius = np.sqrt(x_corr**2 + y_corr**2)
    r_max = max(radius)
    r_min = min(radius)
    theta = np.arcsin(y_corr[np.argmax(radius)] / r_max)
    R = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    v = np.vstack([x_corr, y_corr])
    v_rotated = R @ v
    sigma = r_min / r_max
    v_scaled = np.array([v_rotated[0] * sigma, v_rotated[1]])
    return v_scaled

corrected_mag = soft_iron_calibration(mag_x_corr, mag_y_corr)
mag_x_final, mag_y_final = corrected_mag

# Corrected Yaw Calculation
corrected_yaw = np.arctan2(mag_y_final, mag_x_final)
corrected_yaw[15323:34862] += 5.7
corrected_yaw[48534:61191] += 5.7

# Time calculation
time_sec = imu_data['Header.stamp.secs']
time_nsec = imu_data['Header.stamp.nsecs']
time = time_sec + (time_nsec / 1000000000)

# Gyro Integrated Yaw Calculation
def gyro_integrated_yaw(data, time):
    gyro_int = np.zeros(len(data))
    for i, (start, end) in enumerate([(0, 22000), (22000, 44000), (44000, 58307)]):
        initial = gyro_int[end - 1] if i > 0 else 0
        gyro_int[start:end] = integrate.cumtrapz(data[start:end], time[start:end], initial=initial) * (-1)
    return np.unwrap(gyro_int)

gyro_yaw = gyro_integrated_yaw(imu_data['IMU.angular_velocity.z'], time)

# Plotting Function
def plot_yaw_comparison(time, yaws, labels, colors, title):
    plt.figure(figsize=(16, 8))
    for yaw, label, color in zip(yaws, labels, colors):
        plt.plot(time, yaw, label=label, color=color)
    plt.legend(loc='upper right')
    plt.grid(color='grey', linestyle='--', linewidth=1)
    plt.xlabel('Time')
    plt.ylabel('Yaw (radians)')
    plt.title(title)
    plt.show()

# Raw Yaw vs Calibrated Yaw
plot_yaw_comparison(time, [corrected_yaw, yaw_raw], ["Calibrated Yaw", "Raw Yaw"], ['lightseagreen', 'blue'], 'Estimation of Yaw for Magnetometer')

# Magnetometer Yaw vs Gyro Yaw
plot_yaw_comparison(time, [gyro_yaw, corrected_yaw], ["Gyro Yaw", "Calibrated Yaw"], ['palevioletred', 'lightseagreen'], 'Calibrated Magnetometer Yaw vs Gyro Integrated Yaw')

# Euler from Quaternion
def calculate_euler_angles(data):
    w = data['IMU.orientation.w']
    x = data['IMU.orientation.x']
    y = data['IMU.orientation.y']
    z = data['IMU.orientation.z']
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = np.arctan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    pitch_y = np.arcsin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = np.arctan2(t3, t4)
    return roll_x, pitch_y, yaw_z

roll_x, pitch_y, imu_yaw = calculate_euler_angles(imu_data)

# Applying filters
lpf = filtfilt(*butter(1, 0.05, "lowpass", fs=40, analog=False), corrected_yaw)
hpf = filtfilt(*butter(1, 0.0001, 'highpass', fs=40, analog=False), gyro_yaw)

# Complementary Filter for Yaw
alpha = 0.5
yaw_filtered = np.zeros(len(corrected_yaw))
for i in range(1, len(corrected_yaw)):
    yaw_filtered[i] = alpha * (yaw_filtered[i-1] + gyro_yaw[i]) + (1-alpha) * lpf[i]

# LPF for Yaw vs HPF for gyro vs Complementary Yaw
plt.figure(figsize=(16, 8))
plt.plot(time, lpf, label='LPF Calibrated Yaw', color='teal')
plt.plot(time, hpf, label='HPF Gyro Yaw', color='black')
plt.plot(time, yaw_filtered, label='Complementary Filter Yaw', color='crimson')
plt.legend(loc='upper right')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.xlabel('Time')
plt.ylabel('Yaw (radians)')
plt.title('LPF for Magnetic Yaw vs HPF for Gyro Yaw vs Complementary Filter Yaw')
plt.show()

# Sensor Fusion Yaw vs IMU Yaw
plt.figure(figsize=(16, 8))
plt.plot(time, yaw_filtered, label='Complementary Filter Yaw')
plt.plot(time, imu_yaw*3, label='Yaw computed by IMU')
plt.legend(loc='lower right')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.xlabel('Time')
plt.ylabel('Yaw (radians)')
plt.title('Complementary Filter Yaw vs IMU Yaw')
plt.show()

