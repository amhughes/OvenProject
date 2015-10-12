import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 0.5)
p.start(100)
input('Next Speed')
p.ChangeDutyCycle(75)
input('Next')
p.ChangeDutyCycle(50)
input('Next')
p.ChangeDutyCycle(25)
input('Press return to stop:')   # use raw_input for Python 2
p.stop()
GPIO.cleanup()
