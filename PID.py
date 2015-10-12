#!/usr/bin/python
from max31855 import MAX31855, MAX31855Error
import math
import RPi.GPIO as GPIO
from time import sleep

cs_pin = 8
clock_pin = 11
data_pin = 9
units = "f"
thermocouple = MAX31855(cs_pin, clock_pin, data_pin, units)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
relay = GPIO.PWM(18, 0.5)
relay.start(0)

sp = 130
kp = 1
ki = 1
kd = 1

while 1 = 1:
    T = thermocouple.get()
    Trj = thermocouple.get_rj()
    if T < (Trj-10): break
    In  = T/200
    SpIn = sp/200
    Out = kp*(SpIn-In)
    print(T)
    print(Trj)
    print(Out)
    relay.ChangeDutyCycle(Out)

thermocouple.cleanup()
relay.stop()
GPIO.cleanup()
