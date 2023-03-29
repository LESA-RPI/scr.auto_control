import sys, time
sys.path.append("../catkin_ws/src/scr_control/scripts/lights")
import SCR_OctaLight_client as light_control

# This program aims to turn on lights gradually 


def set_light_brightness(brightness):
    
    #light_control.cct(2, 0, 3500, brightness)
    
    light_control.cct_all(3500, brightness)
    
    '''
    light_control.cct(0, 2, 3500, brightness)
    light_control.cct(0, 0, 3500, brightness)
    light_control.cct(1, 1, 3500, brightness)
    light_control.cct(2, 0, 3500, brightness)
    light_control.cct(2, 2, 3500, brightness)
    light_control.cct(3, 0, 3500, brightness)
    light_control.cct(3, 2, 3500, brightness)
    light_control.cct(4, 1, 3500, brightness)
    light_control.cct(5, 2, 3500, brightness)
    light_control.cct(5, 0, 3500, brightness)
    '''
    

def turn_on_light_gradually(duration=0.5, max_brightness=1000, steps=50):
    step_duration = float(duration) / steps
    brightness_step = max_brightness / steps

    for i in range(steps + 1):
        brightness = int(brightness_step * i)
        set_light_brightness(brightness)
        time.sleep(step_duration)

if __name__ == "__main__":
    start = time.time()
    turn_on_light_gradually()
    end = time.time()
    print(end-start)