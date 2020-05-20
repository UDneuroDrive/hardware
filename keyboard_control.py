from adafruit_servokit import ServoKit
import keyboard
kit = ServoKit(channels=16)

kit.servo[0].set_pulse_width_range(1100, 1900)

steer = 90
throttle = 0
steerinc = 2
throttleinc = 1
maxspeed = 100 # 100 is max

while True:
    if keyboard.is_pressed('left'): 
        if(steer < 180):
            steer = steer + steerinc
    elif keyboard.is_pressed('right'): # is neg
        if(steer > 0):
            steer = steer - steerinc
    else:
        if(steer > 90):
            steer = steer - steerinc
        if(steer < 90):
            steer = steer + steerinc

    if keyboard.is_pressed('up'): 
        if(throttle < maxspeed):
            throttle = throttle + throttleinc
    elif keyboard.is_pressed('down'): # is neg
        if(throttle > -maxspeed):
            throttle = throttle - throttleinc
    else:
        if(throttle > 0):
            throttle = throttle - throttleinc
        if(throttle < 0):
            throttle = throttle + throttleinc
    
    kit.servo[0].angle = steer
    kit.continuous_servo[1].throttle = throttle/100
