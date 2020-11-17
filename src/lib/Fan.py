
from lib.tmp102 import tmp102
from lib.RPi_PWM import RPi_PWM

import time


def get_temp():
    return tmp102.get_temperature()

class Fan():


    def __init__(self):
        self.PIN_FAN = 18
        self.TEMP_START = 24
        self.TEMP_STOP = 22
        
        ### setup pwm
        self.FREQUENCY = 50
        self.PWM_MIN = 40
        self.PWM_MAX = 90
        
        self.pwm = RPi_PWM(self.PIN_FAN, self.FREQUENCY, self.PWM_MIN, self.PWM_MAX, self.PWM_MIN)
        
        ### setup duty
        self.current_temperature = 0
        self.old_temperature = 100
        
        
        self.fan_running = True
   
    
    def run (self):
        while self.fan_running:
            self.current_temperature = get_temp() # current temperature
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
            # not running
            if not self.pwm.is_running() and self.current_temperature > self.TEMP_START:
                self.pwm.start(self.PWM_MIN)   # starts at min speed
                print (f"{current_time} - fan started")
        
            if self.pwm.is_running():
                if self.old_temperature < self.current_temperature and self.pwm.cycle < self.PWM_MAX:
                    self.pwm.cycle += 5
                    
                elif self.current_temperature < self.old_temperature and self.pwm.cycle > self.PWM_MIN:
                    self.pwm.cycle -= 1
                    
                else:
                    self.pwm.cycle += 1
        
                # stop on low temp
                if self.current_temperature <= self.TEMP_STOP:
                    self.pwm.stop()
                    print (f"{current_time} - fan stopped")
            
            if self.DEBUG:
                print (f"{current_time} - temp: {self.current_temperature:.4f}, pwm: {self.pwm.cycle}, fan running: {self.pwm.is_running()}")
        
        self.stop()

    def start(self):
        self.fan_running = True
        self.run()

    def stop(self):
        self.fan_running = False
        self.pwm.stop()
        self.pwm.terminate()


    def get_current_temperature(self):
        return self.current_temperature          



