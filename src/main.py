#!/usr/bin/env python3

import RPi.GPIO as GPIO
import termios, tty, sys, os

from  gpiozero import CPUTemperature #pip
from time import sleep
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_fan = 12 # pin 12, BOARD 18

TEMP_START = 30
TEMP_STOP  = 20

### setup pwm
GPIO.setup(pin_fan, GPIO.OUT)
pwm = GPIO.PWM(pin_fan, 50)
pwm.start(0)
pwm.stop()

### setup cpu temperature
cpu = CPUTemperature()

### setup duty
c = 0
oc = 0
running = True
spinning = False
ot = 100

### some helper functions
def fan_speed(speed):
    pwm.ChangeDutyCycle(speed)
    global spinning 
    spinning = True

def fan_start():
    pwm.start(100)
    global spinning 
    spinning = True

def fan_stop():
    pwm.stop()
    global spinning 
    spinning = False

def get_temp():
    return cpu.temperature


### do the job
while running:
    t = get_temp() # current temperature

    # not running
    if not spinning and t > TEMP_START:
        print ("START FAN!")
        fan_start()   #100
        c = 60

    if spinning and c <= 100 and c >= 60:
        if ot < t: # cpu is getting hotter
            c += 5
        elif t < ot: # cpu is getting colder
            c -= 1
        else:
            pass

        # stop on low temp
        if t < TEMP_STOP:
            c = 0

        if c >= 60:
            if c > 100:
                c = 100 # c max is 100!
            if c != oc:
                fan_speed(c)
        else:
            print ("STOP FAN!")
            fan_stop()

    print (f"temp: {t}, cycle: {c}, spinning: {spinning}")
    ot = t # old temperature
    oc = c
    sleep(1)

# to find an end
pwm.stop()
GPIO.cleanup()
