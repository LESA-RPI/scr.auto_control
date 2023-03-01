import sys
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
import SCR_OctaLight_client as light_control

light_control.cct_all(int(sys.argv[1]), int(sys.argv[2]))
import matplotlib as mpl
mpl.use('Agg')

import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
sys.path.append("../catkin_ws/src/scr_control/scripts/time_of_flight")
import SCR_OctaLight_client as light_control
import SCR_TOF_client as tof
import matplotlib.pyplot as plt


if sys.argv[1] == 'cct_all':
    light_control.cct_all(int(sys.argv[2]), int(sys.argv[3]))
    
elif sys.argv[1] == 'get_distances':
    #print(tof.get_distances(int(sys.argv[2])))
    tof_data_list = tof.get_distances(int(sys.argv[2]))
    
    # Read the ToF sensor data
    for data in tof_data_list: 
        print(data)
    print('Total lists number: {}\nTotal data number in each list: {}'.format(len(tof_data_list),len(tof_data_list[0])))


    # Plot the heatmap
    fig, ax = plt.subplots()
    im = ax.imshow(tof_data_list, cmap='YlOrRd')

    # Customize the plot
    ax.set_xticks(range(len(tof_data_list)))
    ax.set_yticks(range(len(tof_data_list[0])))
    ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'])
    ax.set_yticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Value", rotation=-90, va="bottom")

    # Add a title and axis labels
    ax.set_title("Heatmap Example")
    ax.set_xlabel("X Axis Label")
    ax.set_ylabel("Y Axis Label")

    # Save the plot to a file
    fig.savefig('heatmap.png')


    
elif sys.argv[1] == 'get_distances_all':
    print(tof.get_distances_all())