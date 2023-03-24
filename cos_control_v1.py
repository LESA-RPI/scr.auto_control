import numpy as np
import datetime

import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
sys.path.append("../catkin_ws/src/scr_control/scripts/time_of_flight")
sys.path.append("../catkin_ws/src/scr_control/scripts/color_sensors")
import SCR_OctaLight_client as light_control
import SCR_TOF_client as tof
import SCR_COS_client as cos

result = cos.read(8)

print(result)