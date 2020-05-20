# Import Servo library from Adafruit.
from adafruit_servokit import ServoKit

from picamera import PiCamera

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import Adafruit_MCP3008
import time
from os import path, mkdir

import csv

import led

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

data = []

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(1100, 1900)
# servo 0 -> steering
# servo 1 -> throttle

camera = PiCamera()
camera.resolution = (208, 160)
camera.framerate = 40
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = True
camera.vflip = True

start = False
mode = "training"

steer = 90
throttle = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # choose the pin numbering
GPIO.setup(5, GPIO.IN)

def buttonPressed():
    global mode
    if(mode == "training"):
        mode = "model"
    else:
        mode = "training"

def buttonHeld():
    global start
    start = not start

def button():
    delta = 0
    if (GPIO.input(5) == GPIO.LOW):
        startTime = time.perf_counter()
        while GPIO.input(5) == GPIO.LOW:
            pass
        delta = time.perf_counter() - startTime
    if(delta < 0.5 and delta > 0.05):
        buttonPressed()
    elif (delta >= 0.5): 
        led.off()
        time.sleep(1)
        buttonHeld()

def translate(value = 0, rawMin = 110, rawMax = 218, newMin = 0, newMax = 180):
    # Figure out how 'wide' each range is
    leftSpan = rawMax - rawMin
    rightSpan = newMax - newMin

    valueScaled = float(value - rawMin) / float(leftSpan)

    new = int(newMin + (valueScaled * rightSpan))

    # add end limits so always in range
    if(new < newMin):
        new = newMin
    elif(new > newMax):
        new = newMax
    
    return new


def getControls():
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # return steering and throttle
    # min and max of raw data with current curcuit is min = 110, max = 218
    return translate(value = values[0]), translate(value = values[1], newMin = -100, newMax = 100)
    # print('Steering: {0:>4} | Servo: {1:>4}'.format(*values))

def model():
    return

def training(path, i):
    global data
    steer, throttle = getControls()

    steer = int(steer/10)
    if (throttle > -10 and throttle < 10):
        throttle = 0
    

    steer = steer*10
    # print(steer, throttle)
    kit.servo[0].angle = steer
    kit.continuous_servo[1].throttle = throttle/100
    # print(i,throttle, steer)
    temp = [i,throttle, steer]
    camera.capture(path + str(i) + ".jpg", use_video_port = True)
    data.append(temp)

def getNewPath():
    i = 0
    while True:
        if (path.isdir("/home/sette/neuroDrive/data/" + str(i) + "/")):
            i = i + 1
        else:
            directory = "/home/sette/neuroDrive/data/" + str(i) + "/"
            try:
                mkdir(directory)
            except OSError:
                print ("Creation of the directory %s failed" % directory)
            else:
                print ("Successfully created the directory %s " % directory)
            break
    return directory

def main():
    global data
    i = 0
    path = None
    while True:
        button()
        print(path)
        if(mode == "model"):
            if(len(data) != 0):
                with open(path + "data.csv",'w') as result_file:
                    wr = csv.writer(result_file, delimiter=',')
                    wr.writerow(['number', 'throttle', 'steer'])
                    wr.writerows(data)
                print("done")
                path = None
                data = []
            i = 0
            led.rgb(1,0,0)
            model()
        if(mode == "training"):
            led.rgb(0,1,0)
            print(path)
            if(start == False):
                if(len(data) != 0):
                    with open(path + "data.csv",'w') as result_file:
                        wr = csv.writer(result_file, delimiter=',')
                        wr.writerow(['number', 'throttle', 'steer'])
                        wr.writerows(data)
                    print("done")
                    path = None
                    data = []
                i = 0
            else:
                if(path == None):
                    path = getNewPath()
                i = i + 1
                training(path, i)
main()
