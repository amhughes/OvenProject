#!/usr/bin/python
from max31855.max31855 import MAX31855, MAX31855Error
import math
import RPi.GPIO as GPIO
from time import sleep
import threading

class PIDloop (threading.thread):
    def __init__(self):
        threading.thread.__init__(self)
    def run(self):
        while 1:
            T = thermocouple.get()
            Trj = thermocouple.get_rj()
            if T < (Trj-10) | kill = 1: break
            In  = T/200
            SpIn = sp/200
            Out = kp*(SpIn-In)
            print(T)
            print(Trj)
            print(In)
            print(SpIn)
            print(Out)
            relay.ChangeDutyCycle(Out)
            sleep(1)


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
kp = 100
ki = 1
kd = 1

PIDloopT = PIDloop()

PIDloopT.start()

try:
    PIDloopT.join()
except KeyboardInterrupt:
    kill = 1

thermocouple.cleanup()
relay.stop()
GPIO.cleanup()
print('Done!')
