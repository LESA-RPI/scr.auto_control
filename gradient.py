import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
import SCR_OctaLight_client as light_control

# This program aims to turn on lights gradually 

# Set all lights to given brightness
def set_all_light_brightness(brightness):
    #light_control.cct(2, 0, 3500, brightness)
    light_control.cct_all(3500, brightness)
    
# Set single light to given brightness
def set_light_brightness(light_list, brightness):
    for pos in light_list:
        light_control.cct(pos[0], pos[1], 3500, brightness)

def turn_on_light_gradually(duration=0.5, max_brightness=1000):
    step_duration = 0.025
    steps = int(duration / step_duration)
    brightness_step = max_brightness / steps

    for i in range(steps + 1):
        brightness = int(brightness_step * i)
        set_all_light_brightness(brightness)
        time.sleep(step_duration)

# Set the door-side lights to 1000 brightness  
# and window-side lights to 500 brightness
def initial_light_gradually(duration=0.25, max_brightness=500):
    step_duration = 0.025
    steps = int(duration / step_duration)
    brightness_step = max_brightness / steps

    for i in range(steps + 1):
        brightness = int(brightness_step * i)
        set_all_light_brightness(brightness)
        time.sleep(step_duration)
            
    for i in range(steps, steps*2 + 1):
        brightness = int(brightness_step * i)
        set_light_brightness([[0,0],[0,2],[1,1],[2,0],[2,2]],brightness)
        time.sleep(step_duration)
        
def initial_light_gradually_2(duration=0.25, max_brightness=500):
    step_duration = 0.025
    steps = int(duration / step_duration)
    brightness_step = max_brightness / steps

    for i in range(steps + 1):
        brightness = int(brightness_step * i)
        set_all_light_brightness(brightness)
        time.sleep(step_duration)
            
    set_light_brightness([[0,0],[0,2],[1,1],[2,0],[2,2]],1000)


if __name__ == "__main__":
    start = time.time()
    #turn_on_light_gradually()
    #initial_light_gradually()
    initial_light_gradually_2()
    end = time.time()
    print(end-start)
