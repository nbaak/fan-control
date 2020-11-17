#!/usr/bin/env python3

from tmp102 import tmp102
from lib.RPi_PWM import RPi_PWM

import time

import argparse

def str2bool(value):
    if isinstance(value, bool):
        return value
    
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description="Fan Controler")
parser.add_argument('--debug', dest='DEBUG', type=str2bool, default=True)

args = parser.parse_args()

DEBUG = args.DEBUG

PIN_FAN = 18 # pin 12, BOARD 18

TEMP_START = 24
TEMP_STOP  = 22

### setup pwm
FREQUENCY = 50
PWM_MIN = 40
PWM_MAX = 90

pwm = RPi_PWM(PIN_FAN, FREQUENCY, PWM_MIN, PWM_MAX, PWM_MIN)

### setup duty
running = True
current_temperature = 0
old_temperature = 100

def get_temp():
    return tmp102.get_temperature()


### do the job
while running:
    current_temperature = get_temp() # current temperature

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # not running
    if not pwm.is_running() and current_temperature > TEMP_START:
        pwm.start(PWM_MIN)   # starts at min speed
        print (f"{current_time} - Fan started")

    if pwm.is_running():
        if old_temperature < current_temperature and pwm.cycle < PWM_MAX:
            pwm.cycle += 5
            
        elif current_temperature < old_temperature and pwm.cycle > PWM_MIN:
            pwm.cycle -= 1
            
        else:
            pwm.cycle += 1

        # stop on low temp
        if current_temperature <= TEMP_STOP:
            pwm.stop()
            print (f"{current_time} - Fan stopped")
    
    if DEBUG:
        print (f"{current_time} - temp: {current_temperature:.4f}, pwm: {pwm.cycle}, Fan running: {pwm.is_running()}")
        
    old_temperature = current_temperature # old temperature
    time.sleep(10)

# to find an end
pwm.terminate()

