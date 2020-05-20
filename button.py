import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import led

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # choose the pin numbering
GPIO.setup(5, GPIO.IN)
mode = "training"

def buttonPressed():
    global mode
    if(mode == "training"):
        mode = "model"
    else:
        mode = "training"

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



# GPIO.add_event_detect(5, edge=GPIO.RISING, callback=buttonPressed, bouncetime=200)


while True: # Run forever
    button()
    if(mode == "model"):
        led.rgb(1,0,0)
    if(mode == "training"):
        led.rgb(0,1,0)