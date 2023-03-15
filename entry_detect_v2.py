import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

import datetime

import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
sys.path.append("../catkin_ws/src/scr_control/scripts/time_of_flight")
import SCR_OctaLight_client as light_control
import SCR_TOF_client as tof

# If a data chang above 600 is detected, 
# this function will calculate the direction
# of the movement to confirm there is someone 
# entering the room
def movement_monitor(row_num, cur_mat, old_mat, threshold):
    
    # ----------------------------------------------------- #
    list_calculate_time_start = time.time()
    # ----------------------------------------------------- #
    # Subtraction of each values in two list (1st row)
    data_change_list_1st_row = [b - a for a, b in zip(old_mat[24-row_num], cur_mat[24-row_num])]
    # Subtraction of each values in two list (2nd row)
    data_change_list_2nd_row = [b - a for a, b in zip(old_mat[23-row_num], cur_mat[23-row_num])]
    # Make sure that there is no data change in the 2nd row
    if any(x < threshold for x in data_change_list_2nd_row):

        return False ######################################################## <------ Need to change if there is a bug

    # If the person have not move to the 2nd row yet
    # Get the positions of values that exceed the threshold
    value_above_threshold_pos_1st_row = [i for i in range(len(data_change_list_1st_row)) if data_change_list_1st_row[i] < threshold]
    
    #print(data_change_list_1st_row)
    #print(value_above_threshold_pos_1st_row)
    
    # ----------------------------------------------------- #
    list_calculate_time = time.time() - list_calculate_time_start
    # ----------------------------------------------------- #
    #print("list_calculate_time{}".format(list_calculate_time))
    
    
    # Then, monitor the data change in the second row in 0.1 second
    # Initialize the data matrix
    tof_data_list_2nd_row = tof.get_distances(0)
    tof_data_old_2nd_row = tof_data_list_2nd_row

    # monitor the data change in 0.1 second 
    start_time = time.time() # Get the start time
    change_detected_row_2 = False
    while (time.time() - start_time) < 0.3: # Keep running in 0.1 second
        tof_data_list_2nd_row = tof.get_distances(0)
        # Subtraction of each values in two list (2nd row)
        data_change_list_2nd_row = [b - a for a, b in zip(tof_data_list_2nd_row[24], tof_data_old_2nd_row[23])]
        
        
        #print("row1_data: ", data_change_list_1st_row)
        #print("row2_data: ", data_change_list_2nd_row)
        
        if any(x < threshold for x in data_change_list_2nd_row):
            value_above_threshold_pos_2nd_row = [i for i in range(len(data_change_list_2nd_row)) if data_change_list_2nd_row[i] < threshold]
            
            #print(value_above_threshold_pos_2nd_row)

            
            # Check if there is a value in list_pos2 that is within a difference of 1 from each value in list_pos1
            change_detected_row_2 = any(abs(x - y) < 1 for x in value_above_threshold_pos_1st_row for y in value_above_threshold_pos_2nd_row)
            
            #print(value_above_threshold_pos_1st_row)
            #print(value_above_threshold_pos_2nd_row)
            #rint(change_detected_row_2)
            
            if change_detected_row_2:
                break # The changes detected in row 2, break the while loop
        
        tof_data_old_2nd_row = tof_data_list_2nd_row
            
    return change_detected_row_2
    

def entry_detect(detect_row_count, threshold):
    
    # Initialize the current data matrix
    tof_data_list = tof.get_distances(0) # Store the current data 
    tof_data_origin = tof_data_list # Store the data read from the last iteration

    return_true_count = 0
    
    while(1):
        # read the new data
        tof_data_list = tof.get_distances(0)
        
        # check if there is a data change in the door-side row
        for i in range(len(tof_data_list[24])): 
            if (tof_data_list[24][i] - tof_data_origin[24][i]) <= threshold: # If there's a data change above 600
                #print("1")
                # The function will confirm there is someone get into the room
                for itr in range(detect_row_count-1):
                    if movement_monitor(itr, tof_data_list, tof_data_origin, threshold): 
                        return_true_count += 1
                        #print(return_true_count)
                    else: # The detected signal is a positive error
                        tof_data_origin = tof.get_distances(0) # Update the data matrix and go to the next iteration
                        tof_data_list = tof.get_distances(0)
                        break 
                # At this point: all iterations have been finished,
                # This means the function confirmed that there is 
                # someone get into the room. Then, return True to 
                # send the turning on lights signal 
                if return_true_count == detect_row_count-1:
                    return True
                
        tof_data_origin = tof_data_list # Store the old data matrix
        
    
        

if __name__ == "__main__":

    detect_row_count = int(sys.argv[1])
    threshold = -(int(sys.argv[2]))

    # Open the file for writing
    with open("v2_3_2.txt", "w") as log_file:
        
    
        while(1):
            turn_on_lights = entry_detect(detect_row_count, threshold)
            if turn_on_lights:

                current_time = datetime.datetime.now()
                #log_file.write("Turn on the lights at: {}\n\n".format(current_time))
                print("-------------------Entry detected!-------------------")
                
                light_control.cct(0, 2, 3500, 1000)
                light_control.cct(0, 0, 3500, 1000)
                light_control.cct(1, 1, 3500, 1000)
                light_control.cct(2, 0, 3500, 1000)
                light_control.cct(2, 2, 3500, 1000)
                light_control.cct(3, 0, 3500, 500)
                light_control.cct(3, 2, 3500, 500)
                
                
    
    
    
    #test = tof.get_distances(int(0))
    #print(len(test), len(test[0]))
