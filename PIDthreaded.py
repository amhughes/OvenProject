#!/usr/bin/python
from max31855.max31855 import MAX31855, MAX31855Error
import math
import RPi.GPIO as GPIO
from time import perf_counter
import threading

class PIDloop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        timold = perf_counter()
        Told = thermocouple.get()
        while True:
            tim = perf_counter()
            interr = 0
            if (tim-timold)>1:
                timold = tim
                T = thermocouple.get()
                Trj = thermocouple.get_rj()
                if T < (Trj-10) or kill == 1: break
                err = sp - T
                interr += ki*err
                if interr > outMax:
                    interr = outMax
                elif interr < outMin:
                    interr = outMin
                din = T - Told
                Out = kp*err + interr - kd*din
                if Out > outMax:
                    Out = outMax
                elif Out < outMin:
                    Out = outMin
                print(T)
                print(sp)
                print(Out)
                relay.ChangeDutyCycle(Out)
                Told = T


cs_pin = 8
clock_pin = 11
data_pin = 9
units = "f"
thermocouple = MAX31855(cs_pin, clock_pin, data_pin, units)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
relay = GPIO.PWM(18, 0.5)
relay.start(0)

outMin = 0
outMax = 100
sp = 130
kp = 10
ki = 1
kd = 1
kill = 0


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
