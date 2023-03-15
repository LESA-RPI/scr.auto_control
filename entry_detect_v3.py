import numpy as np
from scipy.signal import medfilt

import datetime

import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
sys.path.append("../catkin_ws/src/scr_control/scripts/time_of_flight")
import SCR_OctaLight_client as light_control
import SCR_TOF_client as tof

import cv2

def control_lights(turn_on):
    if turn_on:
        # Turn on the lights
        #print("On")

        light_control.cct(0, 2, 3500, 1000)
        light_control.cct(0, 0, 3500, 1000)
        light_control.cct(1, 1, 3500, 1000)
        light_control.cct(2, 0, 3500, 1000)
        light_control.cct(2, 2, 3500, 1000)
        light_control.cct(3, 0, 3500, 1000)
        light_control.cct(3, 2, 3500, 1000)

        
    else:
        # Turn off the lights

        light_control.cct(0, 2, 3500, 0)
        light_control.cct(0, 0, 3500, 0)
        light_control.cct(1, 1, 3500, 0)
        light_control.cct(2, 0, 3500, 0)
        light_control.cct(2, 2, 3500, 0)
        light_control.cct(3, 0, 3500, 0)
        light_control.cct(3, 2, 3500, 0)


# Constants
alpha = 0.1  # Smoothing factor for the running average

# Constants
window_size = 5  # Median filter window size
movement_threshold = 150

# Initialize a background matrix with the same shape as your sensor data
background_matrix = np.zeros_like(tof.get_distances(0))

def is_room_occupied():
    global background_matrix
    occupied = False

    for sensor_id in range(18):
        sensor_matrix = np.array(tof.get_distances(sensor_id)).astype(np.uint8)

        # Apply a median filter to the sensor data
        filtered_sensor_matrix = medfilt(sensor_matrix, window_size)

        # Update the background matrix using the filtered sensor data
        background_matrix = (1 - alpha) * background_matrix + alpha * filtered_sensor_matrix

        # Calculate the absolute difference between the filtered sensor data and background matrix
        diff_matrix = np.abs(filtered_sensor_matrix - background_matrix)

        # Check for movement using the threshold
        occupied = occupied or np.any(diff_matrix > movement_threshold)

    return occupied

# Main loop
prev_state_occupied = False
while True:
    room_occupied = is_room_occupied()

    if room_occupied and not prev_state_occupied:
        # Turn lights on
        print("On")
    elif not room_occupied and prev_state_occupied:
        # Turn lights off
        print("Off")

    prev_state_occupied = room_occupied