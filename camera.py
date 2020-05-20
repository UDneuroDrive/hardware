import keyboard
from picamera import PiCamera
import os.path
from os import path
import time

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
camera.hflip = False
camera.vflip = False
# camera.crop = (0.0, 0.0, 1.0, 1.0)

i = 0

while (True):
    if (path.exists("/home/pi/neuroDrive/object_detection/" + str(i) + ".jpg")):
        i = i + 1
    if keyboard.is_pressed('c'): 
        camera.capture('/home/sette/neuroDrive/object_detection/' + str(i) + ".jpg", use_video_port = True)
        print("Captured!")
        i = i + 1
        time.sleep(.5)