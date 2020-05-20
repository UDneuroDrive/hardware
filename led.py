import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # choose the pin numbering

g = 4
r = 12
b = 6

GPIO.setup(r, GPIO.OUT)
GPIO.setup(g, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)

def rgb(red, green, blue):
    if (red==1):
        GPIO.output(r,GPIO.HIGH)
    else:
        GPIO.output(r,GPIO.LOW)

    if (green==1):
        GPIO.output(g,GPIO.HIGH)
    else:
        GPIO.output(g,GPIO.LOW)

    if (blue==1):
        GPIO.output(b,GPIO.HIGH)
    else:
        GPIO.output(b,GPIO.LOW)

def red():
    GPIO.output(r,GPIO.HIGH)

def green():
    GPIO.output(b,GPIO.HIGH)

def blue():
    GPIO.output(g,GPIO.HIGH)

def off():
    GPIO.output(r,GPIO.LOW)
    GPIO.output(g,GPIO.LOW)
    GPIO.output(b,GPIO.LOW)

