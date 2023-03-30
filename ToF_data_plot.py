import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
sys.path.append("../catkin_ws/src/scr_control/scripts/time_of_flight")
sys.path.append("../catkin_ws/src/scr_control/scripts/color_sensors")
import SCR_OctaLight_client as light_control
import SCR_TOF_client as tof
import SCR_COS_client as cos

def plot_data(id):
    matrix = tof.get_distances(id)


    # Create a new figure and axis object
    fig, ax = plt.subplots()

    # Plot the matrix as an image
    im = ax.imshow(matrix, cmap='coolwarm')

    # Add a colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    
    # Loop over the matrix and add text annotations
    for i in range(25):
        for j in range(20):
            text = ax.text(j, i, int(matrix[i][j]/100),
                        ha="center", va="center",
                        fontsize = 7)

    # Set the axis labels
    ax.set_xticks(range(20))
    ax.set_yticks(range(25))

    # Set the tick labels
    ax.set_xticklabels(range(1, 21))
    ax.set_yticklabels(range(1, 26))

    # Set the axis labels
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    # Set the title
    ax.set_title("ToF Data Visualization")
    
    # Save the plot as a PNG file
    plt.savefig('matrix.png')
    

if __name__ == "__main__":
    '''
    while(1):
        plot_data(int(sys.argv[1]))
        print("updated")
    '''
    
    start = time.time()
    while(time.time()-start) < 10: 
        light_control.cct(2,0,3500,0)
