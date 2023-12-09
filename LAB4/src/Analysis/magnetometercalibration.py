import bagpy
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.size': 10})
sns.set_style("dark")
sns.color_palette("viridis", as_cmap=True)

def load_magnetometer_data(bag_file, topic):
    bag = bagpy.bagreader(bag_file)
    data = bag.message_by_topic(topic)
    readings = pd.read_csv(data)
    return readings

def hard_iron_calibration(readings):
    min_x = min(readings['mag_field.magnetic_field.x'])
    max_x = max(readings['mag_field.magnetic_field.x'])
    min_y = min(readings['mag_field.magnetic_field.y'])
    max_y = max(readings['mag_field.magnetic_field.y'])

    x_axis_Offset = (min_x + max_x) / 2.0
    y_axis_Offset = (min_y + max_y) / 2.0
    print("Hard Iron x_axis Offset=", x_axis_Offset)
    print("Hard Iron y_axis Offset=", y_axis_Offset)

    hard_iron_x = readings['mag_field.magnetic_field.x'] - x_axis_Offset
    hard_iron_y = readings['mag_field.magnetic_field.y'] - y_axis_Offset

    return hard_iron_x, hard_iron_y
    
def soft_iron_calibration(hard_iron_x, hard_iron_y):
    data = np.vstack((hard_iron_x, hard_iron_y))
    covariance_matrix = np.cov(data)
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    mean_x, mean_y = np.mean(data[0, :]), np.mean(data[1, :])
    centered_data = data - np.array([[mean_x], [mean_y]])
    rotated_data = eigenvectors.T.dot(centered_data)
    scale_factors = np.sqrt(eigenvalues)
    max_scale = max(scale_factors)
    adjusted_scale_factors = scale_factors / max_scale
    scaled_data = np.diag(1 / adjusted_scale_factors).dot(rotated_data)

    return scaled_data

def plot_data(x, y, title, xlabel, ylabel, color, marker):
    plt.figure(figsize=(10, 8))
    plt.grid(color='grey', linestyle='--', linewidth=1)
    plt.scatter(x, y, marker=marker, label=title, color=color)
    #plt.gca().set_aspect("equal")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='upper right')
    plt.show()

# Load magnetometer data
readings = load_magnetometer_data('/home/steffit/Downloads/EECE5554/LAB4/src/Data/data_going_in_circles.bag', '/imu')

# Perform Hard-Iron Calibration
hard_iron_x, hard_iron_y = hard_iron_calibration(readings)

# Perform Soft-Iron Calibration
calibrated_data = soft_iron_calibration(hard_iron_x, hard_iron_y)

# Plotting
plot_data(readings['mag_field.magnetic_field.x'], readings['mag_field.magnetic_field.y'], 'Raw/Uncalibrated Data', 'Magnetic Field X', 'Magnetic Field Y', 'brown', '.')
plot_data(hard_iron_x, hard_iron_y, 'Hard-Iron Calibrated Data', 'Hard_Iron_X (Guass)', 'Hard_Iron_Y (Guass)', 'darkgreen', '+')
plot_data(calibrated_data[0], calibrated_data[1], 'Soft-Iron Calibrated Data', 'Soft_Iron_X (Guass)', 'Soft_Iron_Y (Guass)', 'palevioletred', 'x')

# Plot Raw vs Calibrated Data
plt.figure(figsize=(10, 8))
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.scatter(readings['mag_field.magnetic_field.x'], readings['mag_field.magnetic_field.y'], marker='.', label='Raw/Uncalibrated Data', color='blue')
plt.scatter(calibrated_data[0], calibrated_data[1], marker='+', label='Calibrated Data', color='red')
#plt.gca().set_aspect("equal")
plt.title('Raw vs Calibrated Data')
plt.xlabel('Magnetic Field X (Guass)')
plt.ylabel('Magnetic Field Y (Guass)')
plt.legend()
plt.show()
