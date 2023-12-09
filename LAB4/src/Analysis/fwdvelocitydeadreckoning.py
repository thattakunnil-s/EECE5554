import bagpy
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from bagpy import bagreader
import scipy.integrate as integrate
from scipy.interpolate import interp1d

# Set plot style
sns.set_style("dark")
sns.color_palette("viridis", as_cmap=True)
plt.rcParams.update({'font.size': 10})

# Read data from bag files
bag = bagreader('/home/steffit/Downloads/EECE5554/LAB4/src/Data/data_driving.bag')
imu_data_path = bag.message_by_topic('/imu')
gps_data_path = bag.message_by_topic('/gps')

imu_data = pd.read_csv(imu_data_path)
gps_data = pd.read_csv(gps_data_path)

# Calculate time from IMU data
imu_secs = imu_data['Header.stamp.secs']
imu_nsecs = np.double(imu_data['Header.stamp.nsecs']) / 1000000000
imu_time = np.double(imu_secs) + imu_nsecs

# Function to calculate IMU velocity
def calculate_imu_velocity(data):
    linear_acceleration = data['IMU.linear_acceleration.x'] - np.mean(data['IMU.linear_acceleration.x'])
    velocity_difference = np.diff(linear_acceleration) / 0.025
    adjusted_acceleration = linear_acceleration[1:] - velocity_difference
    adjusted_velocity = integrate.cumtrapz(adjusted_acceleration, initial=0)
    adjusted_velocity[adjusted_velocity < 0] = 0
    raw_velocity = integrate.cumtrapz(linear_acceleration, initial=0)
    return raw_velocity, adjusted_velocity

raw_velocity, adjusted_velocity = calculate_imu_velocity(imu_data)

# GPS velocity calculation
gps_time = gps_data['Header.stamp.secs']
UTM_easting = gps_data['UTM_easting']
UTM_northing = gps_data['UTM_northing']
gps_distances = [math.sqrt((UTM_northing[i + 1] - UTM_northing[i])**2 + (UTM_easting[i + 1] - UTM_easting[i])**2) for i in range(len(UTM_northing) - 1)]
gps_velocity = np.array(gps_distances) / np.diff(gps_time)

# Plotting function
def plot_velocity(time, velocity, title, label, color):
    plt.figure(figsize=(16, 8))
    plt.plot(time, velocity, label=label, color=color)
    plt.legend(loc='upper right')
    plt.grid(color='grey', linestyle='--', linewidth=1)
    plt.title(title)
    plt.xlabel('Time (secs)')
    plt.ylabel('Velocity (m/sec)')
    plt.show()

# Plot raw velocity from GPS
plot_velocity(gps_data['Time'][1:], gps_velocity * 2000000, 'Forward velocity from GPS', 'GPS Raw Velocity', 'green')

# Plot raw velocity from IMU
plot_velocity(imu_time, raw_velocity, 'Forward velocity from IMU before adjustment', 'IMU Raw Velocity', 'blue')

# Plot corrected velocity from IMU
plot_velocity(imu_time[1:], adjusted_velocity / 1000, 'Forward velocity from IMU after adjustment', 'IMU Adjusted Velocity', 'red')

# Plot velocity from IMU before and after adjustment
plt.figure(figsize=(16, 8))
plt.plot(imu_time[1:], adjusted_velocity, label='IMU Adjusted Velocity', c='red')
plt.plot(imu_time, raw_velocity, label='IMU Raw Velocity', c='blue')
plt.legend(loc='upper right')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.title('Forward velocity from IMU before and after adjustment')
plt.xlabel('Time (secs)')
plt.ylabel('Velocity (m/sec)')
plt.show()

# Displacement
disp_x = integrate.cumtrapz(adjusted_velocity, initial=0)
int_gps_vel = integrate.cumtrapz(gps_velocity, initial=0)

# Y_observed vs wX(dot)
accex = imu_data['IMU.linear_acceleration.x']
timeimu = imu_data['Header.stamp.secs']+imu_data['Header.stamp.nsecs']*10e-9
x2dot = accex
x1dot = integrate.cumtrapz(x2dot)
angz = imu_data['IMU.angular_velocity.z']
y2dot = angz[1:] * x1dot
Y_observed = imu_data['IMU.linear_acceleration.y']

plt.figure(figsize=(8, 8))
plt.plot(Y_observed, label='Y observed', c='blue')
plt.plot(y2dot/1000, label='wX(dot)', c='red')
plt.legend(loc='upper right')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.title('Y_observed vs wX(dot)')
plt.xlabel('Time')
plt.ylabel('Acceleration')
plt.show()

# Trajectory of Vehicle
w = imu_data['IMU.orientation.w']
x = imu_data['IMU.orientation.x']
y = imu_data['IMU.orientation.y']
z = imu_data['IMU.orientation.z']

# Euler from Quaternion(x, y, z, w):
t0 = +2.0 * (w * x + y * z)
t1 = +1.0 - 2.0 * (x * x + y * y)
roll_x = np.arctan2(t0, t1)

t2 = +2.0 * (w * y - z * x)
pitch_y = np.arcsin(t2)

t3 = +2.0 * (w * z + x * y)
t4 = +1.0 - 2.0 * (y * y + z * z)
yaw_z = np.arctan2(t3, t4)

fv = np.unwrap(adjusted_velocity)
mgh1 = yaw_z
rot = (-108*np.pi/180)

unit1 = np.cos(mgh1[1:]+rot)*fv
unit2 = -np.sin(mgh1[1:]+rot)*fv
unit3 = np.cos(mgh1[1:]+rot)*fv
unit4 = np.sin(mgh1[1:]+rot)*fv
ve = unit1+unit2
vn = unit3+unit4
xe = integrate.cumtrapz(ve)
xn = integrate.cumtrapz(vn)

plt.figure(figsize=(8, 8))
plt.plot((xe/(10**6))/2, -xn/(10**5), c='blue')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.title('Trajectory of Vehicle')
plt.xlabel('Xe')
plt.ylabel('Xn')
plt.show()

plt.figure(figsize=(8, 8))
plt.plot(UTM_easting, UTM_northing, c='red')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.title('UTM Easting vs UTM Northing')
plt.xlabel('UTM Easting')
plt.ylabel('UTM Northing')
plt.show()

# Combined plots
f, ax = plt.subplots(3, 1, figsize=(30, 18))
f.subplots_adjust(hspace=0.4)
ax[0].plot(Y_observed, label='Y observed', c='blue')
ax[0].plot(y2dot/1000, label='wX(dot)', c='red')
ax[1].plot((xe/(10**6))/2, -xn/(10**5), c='blue')
ax[2].plot(UTM_easting, UTM_northing, c='red')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Acceleration (m/s^2)')
ax[0].set_title('Y_observed vs wX(dot)')
ax[1].set_xlabel('Xe')
ax[1].set_ylabel('Xn')
ax[1].set_title('Trajectory of Vehicle')
ax[2].set_xlabel('UTM Easting')
ax[2].set_ylabel('UTM Northing')
ax[2].set_title('UTM Easting vs UTM Northing')
plt.show()

# Observed lateral acceleration from IMU
y_obs_dotdot = imu_data['IMU.linear_acceleration.y']
f = interp1d(gps_time[:-1], gps_velocity, fill_value="extrapolate")
X_dot_aligned = f(imu_time)

# Angular velocity (omega)
omega = imu_data['IMU.angular_velocity.z']

# Calculate the rate of change of angular velocity (omega dot)
omega_dot = np.diff(omega) / np.diff(imu_time)
omega_dot = np.append(omega_dot, 0)  

# Calculate xc
xc = (y_obs_dotdot - omega * X_dot_aligned) / omega_dot
xc[abs(omega_dot) < 1e-4] = np.nan  
xc_valid = xc[np.isfinite(xc) & (xc > 0)]  # Assuming xc should be positive
estimated_xc = np.mean(xc_valid) if len(xc_valid) > 0 else np.nan
print("Estimated Lateral Displacement of IMU from Vehicle's CM (xc):", estimated_xc)
