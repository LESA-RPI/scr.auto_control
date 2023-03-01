import matplotlib
matplotlib.use('Agg')

import sys, time
import curses
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
sys.path.append("../catkin_ws/src/scr_control/scripts/time_of_flight")
import SCR_OctaLight_client as light_control
import SCR_TOF_client as tof

import matplotlib.pyplot as plt



if sys.argv[1] == 'change_monitor':
    
    # Initialize the curses library
    stdscr = curses.initscr()

    # Don't echo user input to the screen
    curses.noecho()

    # Don't wait for the Enter key to be pressed
    curses.cbreak()

    # Enable special keys, like arrow keys and function keys
    stdscr.keypad(True)
    
    tof_data_list = tof.get_distances(int(sys.argv[2]))

    # store the current data in the ToF matrix
    tof_origin = tof_data_list
    
    # detect the new data from the ToF sensor in the loop
    # and return the changes of data 
    loop_times = 0
    
    
    while (loop_times<10):
        max_change = 0
        
        # create a new matrix to store the changes of data
        one_data_change_list = [0]*len(tof_data_list[0])
        data_change_matrix = [one_data_change_list]*len(tof_data_list)
        # read the new data matrix
        tof_data_list = tof.get_distances(int(sys.argv[2]))
        # calculate and store the changes
        for i in range(0, len(tof_data_list)): 
            for j in range(0, len(tof_data_list[0])):
                data_change_matrix[i][j] = tof_data_list[i][j] - tof_origin[i][j]
                if abs(max_change) < abs(data_change_matrix[i][j]):
                    max_change = data_change_matrix[i][j]
                    
        
        # update the data matrix
        tof_origin = tof_data_list
        # Move the cursor back to the beginning of the line
        stdscr.move(0, 0)

        # Print the updated countdown value
        stdscr.addstr("max_change={}{}".format(max_change,data_change_matrix))

        # Refresh the screen to show the updated text
        stdscr.refresh()

        time.sleep(1)
        loop_times += 1
        
        
        '''
        sys.stdout.write('\r{}'.format(data_change_matrix))
        sys.stdout.flush()
        time.sleep(1)
        '''
    # Clean up the curses library before exiting
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

elif sys.argv[1] == 'max_change':
    tof_data_list = tof.get_distances(int(sys.argv[2]))

    # store the current data in the ToF matrix
    tof_origin = tof_data_list
    
    # detect the new data from the ToF sensor in the loop
    # and return the changes of data 
    while (1):
        max_change = 0
        max_change_output = ""
        # create a new matrix to store the changes of data
        one_data_change_list = [0]*len(tof_data_list[0])
        data_change_matrix = [one_data_change_list]*len(tof_data_list)
        # read the new data matrix
        tof_data_list = tof.get_distances(int(sys.argv[2]))
        # calculate and store the changes
        for i in range(0, len(tof_data_list)): 
            for j in range(0, len(tof_data_list[0])):
                data_change_matrix[i][j] = tof_data_list[i][j] - tof_origin[i][j]
                if abs(max_change) < abs(data_change_matrix[i][j]) and i != 1 and j != 19:
                    max_change = data_change_matrix[i][j]
                    max_change_output = "{} i={} j={}".format(data_change_matrix[i][j],i,j)
        print(max_change_output)
        tof_origin = tof_data_list
        time.sleep(1)


elif sys.argv[1] == 'change_freq':
    tof_data_list = tof.get_distances(int(sys.argv[2]))
    
    change_freq_matrix = [[[] for j in range(len(tof_data_list[0]))] for i in range(len(tof_data_list))]

    # store the current data in the ToF matrix
    tof_origin = tof_data_list
    
    time.sleep(0.1)
    
    # detect the new data from the ToF sensor in the loop
    # and return the changes of data 
    for loop_times in range(0, 10):
        max_change = 0
        max_change_i = 0 
        max_change_j = 0 
        
        max_change_output = ""
        # create a new matrix to store the changes of data
        data_change_matrix = [[0]*len(tof_data_list[0]) for i in range(len(tof_data_list))]
        # read the new data matrix
        tof_data_list = tof.get_distances(int(sys.argv[2]))
        
        # calculate and store the changes
        for i in range(0, len(tof_data_list)): 
            for j in range(0, len(tof_data_list[0])):
                data_change_matrix[i][j] = abs(tof_data_list[i][j] - tof_origin[i][j])
                if loop_times != 0:
                    (change_freq_matrix[i][j]).append(data_change_matrix[i][j])

        
        tof_origin = tof_data_list
        time.sleep(0.1)
    
    #print(change_freq_matrix)
    
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
        
    #print(mean_change)
        
    # sort and print the mean_change matrix
    sorted_mean_change = sorted(mean_change, key=lambda x: -x[0])
    #print(sorted_mean_change)
    
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
    plt.title('Average changes of ToF sensor {}'.format(sys.argv[2]))

    # Show the chart
    plt.savefig('ToF{}_error_bar_chart.png'.format(sys.argv[2]))
    
    
    
'''
    print("==========================================")
    print(len(plot_max_list_x))
    print("++++++++++++++++++++++++++++++++++++++++++")
    print(len(plot_max_list_y))
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
'''