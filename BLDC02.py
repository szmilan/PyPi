from time import sleep
import pigpio
from read_RPM import reader
import RPi.GPIO as GPIO
import QuadNumeric
import cv2

# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi()

# Calibrate ESC
ESC_GPIO = 13



# Set up input pins for thumbwheel switch
try:
    while 1:
        speed = 1.5			

        k = cv2.waitKey(1) & 0xFF
	
	pi.set_servo_pulsewidth(ESC_GPIO, speed * 1000 / 7 + 1000)
	
        sleep(100)

finally:
    pi.set_servo_pulsewidth(ESC_GPIO, 0) # Stop servo pulses.
    pi.stop() # Disconnect pigpio.
