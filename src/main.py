#!/usr/bin/env python3

import RPi.GPIO as GPIO
import termios, tty, sys, os

#from gpiozero import CPUTemperature #pip
from tmp102 import tmp102
from time import sleep
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN_FAN = 18 # pin 12, BOARD 18

TEMP_START = 24
TEMP_STOP  = 22

### setup pwm
FREQUENCY = 50
PWM_MIN = 30
PWM_MAX = 90

GPIO.setup(PIN_FAN, GPIO.OUT)
pwm = GPIO.PWM(PIN_FAN, FREQUENCY) # Pin, Hz

### setup duty
pwm_cycle = 0
old_pwm = 0
running = True
spinning = False
old_temperature = 100

### some helper functions
def fan_speed(speed):
    pwm.ChangeDutyCycle(speed)
    global spinning 
    spinning = True

def fan_start():
    global spinning
    pwm.start(PWM_MIN) 
    pwm.ChangeFrequency(FREQUENCY)  # don't know why, but now its working
    spinning = True

def fan_stop():
    pwm.stop()
    global spinning 
    spinning = False

def get_temp():
    return tmp102.get_temperature()


### do the job
while running:
    current_temperature = get_temp() # current temperature

    # not running
    if not spinning and current_temperature > TEMP_START:
        print ("START FAN!")
        fan_start()   # starts at min speed
        pwm_cycle = PWM_MIN

    if spinning and pwm_cycle <= PWM_MAX and pwm_cycle >= PWM_MIN:
        if old_temperature <= current_temperature:
            pwm_cycle += 5
        elif current_temperature < old_temperature:
            pwm_cycle -= 1
        else:
            print ("do nothing")

        # stop on low temp
        if current_temperature < TEMP_STOP:
            pwm_cycle = 0

        if pwm_cycle >= PWM_MIN:
            if pwm_cycle > PWM_MAX:
                pwm_cycle = PWM_MAX # pwm max is 100!
                
            if pwm_cycle != old_pwm:
                fan_speed(pwm_cycle)
                
        else:
            print ("STOP FAN!")
            fan_stop()

    print (f"temp: {current_temperature}, pwm: {pwm_cycle}, spinning: {spinning}")
    old_temperature = current_temperature # old temperature
    old_pwm = pwm_cycle
    sleep(5)

# to find an end
pwm.stop()
GPIO.cleanup()
