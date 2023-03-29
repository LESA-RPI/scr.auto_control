import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
import SCR_OctaLight_client as light_control

# The function will turn on the lights on (1,1) and (4,1)
# with 1000 brightness and turn on the other lights with 
# 500 brightness

def central_lights(door_side=True, window_side=True):
    if door_side:
        light_control.cct(1, 1, 3500, 1000)
        light_control.cct(0, 0, 3500, 500)
        light_control.cct(0, 2, 3500, 500)
        light_control.cct(2, 0, 3500, 500)
        light_control.cct(2, 2, 3500, 500)
        
    if window_side:
        light_control.cct(4, 1, 3500, 1000)
        light_control.cct(3, 0, 3500, 500)
        light_control.cct(3, 2, 3500, 500)
        light_control.cct(5, 0, 3500, 500)
        light_control.cct(5, 2, 3500, 500)
    

if __name__ == "__main__":
    central_lights()