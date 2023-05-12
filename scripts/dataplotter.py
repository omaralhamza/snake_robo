import matplotlib.pyplot as plt
import argparse

# create an argument parser
parser = argparse.ArgumentParser()

# add the filename argument
parser.add_argument("filename", help="name of the file")

# parse the arguments
args = parser.parse_args()

# get the filename from the arguments
filename = args.filename
# read the data from the file
data_file = open('logs/'+ filename + '.txt', "r")
data_lines = data_file.readlines()

# initialize the data arrays
time = []
acceleration = []
position_setpoint = []
position_setpoint_error = []
velocity_setpoint = []
velocity_setpoint_error = []

# parse the data lines and store the values in the arrays
for line in data_lines[1:]:
    line = line.strip().split(",")
    time.append(float(line[0]))
    acceleration.append(float(line[1]))
    position_setpoint.append(float(line[2]))
    position_setpoint_error.append(float(line[3]))
    velocity_setpoint.append(float(line[4]))
    velocity_setpoint_error.append(float(line[5]))

# create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

# plot acceleration and velocity in the first subplot
ax1.plot(time, position_setpoint, label="position_setpoint")
ax1.plot(time, position_setpoint_error, label="position_setpoint_error")
ax1.set_ylabel("Position Data")
ax1.legend()

# plot velocity error and position setpoint error in the second subplot
ax2.plot(time, velocity_setpoint, label="velocity_setpoint")
ax2.plot(time, velocity_setpoint_error, label="velocity_setpoint_error")
ax2.set_ylabel("Velocity Data")
ax2.set_xlabel("Time")
ax2.legend()

# create a twin axis for position setpoint in the second subplot
ax2_2 = ax2.twinx()
ax2_2.plot(time, acceleration, label="acceleration", color='C4')
ax2_2.set_ylabel("Acceleration Data")
ax2_2.legend()

plt.show()