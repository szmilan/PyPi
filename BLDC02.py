from time import sleep
import pigpio
from read_RPM import reader
import RPi.GPIO as GPIO
import QuadNumeric


# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi() 

# Calibrate ESC
ESC_GPIO = 13
pi.set_servo_pulsewidth(ESC_GPIO, 2000) # Maximum throttle.
sleep(2)
pi.set_servo_pulsewidth(ESC_GPIO, 1000) # Minimum throttle.
sleep(2)

# Set up input pins for thumbwheel switch
BCD = [16,20,21]
for pin in BCD:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
