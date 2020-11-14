#!/usr/bin/env python3

from tmp102 import tmp102
from RPi_PWM import RPi_PWM

from time import sleep


PIN_FAN = 18 # pin 12, BOARD 18

TEMP_START = 24
TEMP_STOP  = 22

### setup pwm
FREQUENCY = 50
PWM_MIN = 30
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

    # not running
    if not pwm.is_running() and current_temperature > TEMP_START:
        pwm.start(PWM_MIN)   # starts at min speed

    if pwm.is_running():
        if old_temperature <= current_temperature and pwm.cycle < PWM_MAX:
            pwm.cycle += 5
            
        elif current_temperature < old_temperature and pwm.cycle > PWM_MIN:
            pwm.cycle -= 1
            
        else:
            pass

        # stop on low temp
        if current_temperature <= TEMP_STOP:
            pwm.stop()

    print (f"temp: {current_temperature:.4f}, pwm: {pwm.cycle}, fan running: {pwm.is_running()}")
    old_temperature = current_temperature # old temperature
    sleep(10)

# to find an end
pwm.terminate()

