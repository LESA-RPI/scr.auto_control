import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import datetime
from gradient import *

import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
sys.path.append("../catkin_ws/src/scr_control/scripts/time_of_flight")
sys.path.append("../catkin_ws/src/scr_control/scripts/color_sensors")
import SCR_OctaLight_client as light_control
import SCR_TOF_client as tof
import SCR_COS_client as cos


# This function will detect the sensor pixel 
# with a high noise level. Then, these pixels 
# will be ignored in the auto_control algorithm.   

def tof_pixel_check(tof_id, loop_count=100, freq=0.1, threshold=500, bar_chart=True, grid=True, bar_fn="ToF_bar_chart.png", grid_fn="ToF_grid_figure.png"):
    
    tof_data_list = tof.get_distances(tof_id)
    
    change_freq_matrix = [[[] for j in range(len(tof_data_list[0]))] for i in range(len(tof_data_list))]

    # store the current data in the ToF matrix
    tof_origin = tof_data_list
    
    
    # detect the new data from the ToF sensor in the loop
    # and return the changes of data 
    for itr_number in range(0, loop_count):
        max_change = 0
        max_change_i = 0 
        max_change_j = 0 
        
        max_change_output = ""
        # create a new matrix to store the changes of data
        data_change_matrix = [[0]*len(tof_data_list[0]) for i in range(len(tof_data_list))]
        # read the new data matrix
        tof_data_list = tof.get_distances(int(tof_id))
        
        # calculate and store the changes
        for i in range(0, len(tof_data_list)): 
            for j in range(0, len(tof_data_list[0])):
                data_change_matrix[i][j] = abs(tof_data_list[i][j] - tof_origin[i][j])
                if itr_number != 0:
                    (change_freq_matrix[i][j]).append(data_change_matrix[i][j])

        
        tof_origin = tof_data_list
        time.sleep(freq)

    
    # calcualte the average changes for each pixel
    mean_change = []
    
    for i in range(0, len(change_freq_matrix)):
        for j in range(0, len(change_freq_matrix[0])):
            
            each_pixel_change = []
            
            mean_change_one_pixel = sum(change_freq_matrix[i][j])/len(change_freq_matrix[i][j])
            maximum_change = max(change_freq_matrix[i][j])
            
            each_pixel_change.append(mean_change_one_pixel)
            each_pixel_change.append(maximum_change)
            each_pixel_change.append(i)
            each_pixel_change.append(j)
            
            mean_change.append(each_pixel_change)
        


    # sort the mean_change matrix
    sorted_mean_change = sorted(mean_change, key=lambda x: -x[0])
    
    
    # Plot the bar chart
    if bar_chart: 
        # plot the maximum_change and mean_change amoung these pixels
        plot_max_list_x = []
        plot_max_list_y = []

        
        for d in sorted_mean_change:
            plot_max_list_x.append(str(d[2])+str(d[3]))
            plot_max_list_y.append(int(d[1])) # insert the max_changes

        
        plt.bar(plot_max_list_x, plot_max_list_y)

        # Add labels
        plt.xlabel('Pixel locations')
        plt.ylabel('Average changes')
        plt.title('Average changes of ToF sensor {}'.format(tof_id))

        # Save the chart
        plt.savefig(bar_fn)

    # Plot the grid
    if grid:  
        # Create a new martix to store the max changes values
        max_change_matrix = [[0 for j in range(20)] for i in range(25)]
        for i in range(0, len(change_freq_matrix)):
            for j in range(0, len(change_freq_matrix[0])):
                max_change_matrix[i][j] = max(change_freq_matrix[i][j])


        # Create a new figure and axis object
        fig, ax = plt.subplots()

        # Plot the matrix as an image
        im = ax.imshow(max_change_matrix, cmap='coolwarm')

        # Add a colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        
        # Loop over the matrix and add text annotations
        for i in range(25):
            for j in range(20):
                text = ax.text(j, i, max_change_matrix[i][j],
                            ha="center", va="center",
                            fontsize = 5,
                            fontweight='bold' if max_change_matrix[i][j] >= threshold else 'normal',
                            color="black" if max_change_matrix[i][j] < threshold else "white")

        # Set the axis labels
        ax.set_xticks(range(20))
        ax.set_yticks(range(25))

        # Set the tick labels
        ax.set_xticklabels(range(1, 26))
        ax.set_yticklabels(range(1, 21))

        # Set the axis labels
        ax.set_xlabel("Column")
        ax.set_ylabel("Row")

        # Set the title
        ax.set_title("ToF Matrix Visualization")
        
        # Add the threshold value as text outside the matrix
        ax.text(1.32, 1.0, "Threshold:\n   {}".format(threshold),
        transform=ax.transAxes,
        fontsize=10,
        ha='left',
        va='center')

        # Save the figure to a file
        plt.savefig(grid_fn)
        
        # Return the matrix of selected pixel
        selected_pixel = np.zeros((25,20))
        
    for i in range(0, len(max_change_matrix)):
        for j in range(0, len(max_change_matrix[0])):
            if max_change_matrix[i][j] < threshold:
                selected_pixel[i, j] = True
            else: 
                selected_pixel[i, j] = False
    
    
    # Set pixels to False manually
    for i in range(22, 25):
        selected_pixel[i, 19] = False
    selected_pixel[23, 18] = False
    
    return selected_pixel
    
def check_neighbors(matrix, row, col):
    rows, cols = len(matrix), len(matrix[0])
    #top = matrix[row-1][col] if row > 0 else 2000
    bottom = matrix[row+1][col] if row < rows-1 else 2000
    left = matrix[row][col-1] if col > 0 else 2000
    right = matrix[row][col+1] if col < cols-1 else 2000
    
    return bottom <= 2700 and left <= 2700 and right <= 2700
    
    
def entry_detect(pixel_pick_mat, start=False):
    if start == False: 
        return None
    

    # read the new data
    tof_data_list = tof.get_distances(0)
    
    trigger = False
    
    j = 0
    
    for pixel in tof_data_list[24]:
        #print(tof_data_list[24])
        if pixel <= 2000 and pixel_pick_mat[24][j]: 
            trigger = True
            break
        j += 1
    
    if not trigger:
        return False
    
    # If the data read by door-side pixels is lower than 2500
    # This means someone may get into the room. 
    
    # Then, in 1 second period, detect the change of each pixel, 
    # If there are more than 5 pixels have a change lower than
    # -500, the lights will turn on. 
    
    tof_data_origin = tof_data_list # Store the old values
    
    start_time = time.time() # Get the start time
    pixel_change_count = 0 # Count the number of pixels with a high change

    #print("Enter 2s while loop")
    while (time.time() - start_time) < 2: # Keep running in 2 seconds
        
        tof_data_list = tof.get_distances(0) # Update the values
        
        # create a new matrix to store the changes of data
        #data_change_matrix = np.zeros((25,20))
        
        # calculate and compare the changes
        for i in range(22, 25): 
            for j in range(0, 20):
                change = tof_data_list[i][j] - tof_data_origin[i][j]
                #data_change_matrix[i, j] = change
                if (change <= -500)\
                and (pixel_pick_mat[i][j]):
                #and check_neighbors(tof_data_list, i, j):
                    
                    pixel_change_count += 1
                    print("distance change <= -500 detected on: {} {} at {}".format(i, j, datetime.datetime.now()))
                    log_file.write("distance change <= -500 detected on: {} {} at {}".format(i, j, datetime.datetime.now()))
                    if pixel_change_count >= 3:

                        return True


        tof_data_origin = tof_data_list


def turn_lights_on(gradient_trigger):
    if gradient_trigger:
        turn_on_light_gradually()
        

    else:
        light_control.cct(0, 2, 3500, 1000)
        light_control.cct(0, 0, 3500, 1000)
        light_control.cct(1, 1, 3500, 1000)
        light_control.cct(2, 0, 3500, 1000)
        light_control.cct(2, 2, 3500, 1000)
        light_control.cct(3, 0, 3500, 500)
        light_control.cct(3, 2, 3500, 500)
        light_control.cct(4, 1, 3500, 500)
        light_control.cct(5, 2, 3500, 500)
        light_control.cct(5, 0, 3500, 500)
        


def sleep_helper(log_file):
    
    sleep_timer = time.time()

    while(time.time() - sleep_timer) < 60:
        # If the light is turned on manually
        if not (all(value == 0.0 for value in light_control.get_sources(0, 0))): 
            print("Lights are turned on during sleep, auto_control enabled {}".format(datetime.datetime.now()))
            log_file.write("Lights are turned on during sleep, auto_control enabled {}".format(datetime.datetime.now()))
            return True
    
    print("1 min is up, auto_control enabled {}".format(datetime.datetime.now()))
    log_file.write("1 min is up, auto_control enabled {}".format(datetime.datetime.now()))
    return False

if __name__ == "__main__":

    print("System is initializing, please make sure there's no movement near the door")
    pixel_pick_mat = tof_pixel_check(0, bar_chart=False)
    sleep_flag = False
    print("System Initialized")
    print("auto_control system is running")
    
    # Open the file for writing
    with open("auto_control_log.txt", "w") as log_file:
        
        # While the light is off
        while True:
            light_is_off = all(value == 0.0 for value in light_control.get_sources(0, 0))

            # Check if the light is manually turned on and set sleep_flag to True
            if not light_is_off:
                sleep_flag = True

            # sleep for 60 second:
            if light_is_off and sleep_flag:
                print("Lights are turned off, disable auto_control for 1 minute {}".format(datetime.datetime.now()))
                log_file.write("Lights are turned off, disable auto_control for 1 minute {}".format(datetime.datetime.now()))
                sleep_flag = sleep_helper(log_file)
            
            light_is_off = all(value == 0.0 for value in light_control.get_sources(0, 0))
            
            while light_is_off:
                turn_on_lights = entry_detect(pixel_pick_mat, True)
                if turn_on_lights:
                    turn_lights_on(True)
                    sleep_flag = True
                    current_time = datetime.datetime.now()
                    log_file.write("Turn on the lights at: {}\n".format(current_time))
                    print("Turn lights on at {}\n".format(current_time))
                    
                light_is_off = all(value == 0.0 for value in light_control.get_sources(0, 0))


