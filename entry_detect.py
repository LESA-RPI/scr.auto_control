import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
sys.path.append("../catkin_ws/src/scr_control/scripts/time_of_flight")
import SCR_OctaLight_client as light_control
import SCR_TOF_client as tof

def tof_pixel_check(tof_id, loop_count=10, freq=0.1, ignore_percentage=20, bar_chart=True, grid=True, bar_fn="ToF_bar_chart.png", grid_fn="ToF_grid_figure.png"):
    tof_data_list = tof.get_distances(tof_id)
    
    change_freq_matrix = [[[] for j in range(len(tof_data_list[0]))] for i in range(len(tof_data_list))]

    # store the current data in the ToF matrix
    tof_origin = tof_data_list
    
    time.sleep(0.1)
    
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
        # Calculate the threshold value
        extracted_pixel_number = int(500*ignore_percentage/100)
        # The value above this threshold will be highlighted
        threshold = sorted_mean_change[extracted_pixel_number-1][1]
        
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
        
        print("===================\n\n")
        print(len(change_freq_matrix), len(change_freq_matrix[0]))
        print("\n\n===================")

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


if __name__ == "__main__":
    tof_pixel_check(int(sys.argv[1]),bar_chart=False)