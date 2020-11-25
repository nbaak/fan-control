
from lib.tmp102 import tmp102
from lib.RPi_PWM import RPi_PWM

import time


def get_temp():
    return tmp102.get_temperature()

class Fan():


    def __init__(self, debug = True):
        self.PIN_FAN = 18
        self.TEMP_START = 24
        self.TEMP_STOP = 22
        
        ### setup pwm
        self.FREQUENCY = 50
        self.PWM_MIN = 40
        self.PWM_MAX = 90
        
        self.pwm = None
        self.setup_gpio()
        
        ### setup duty
        self.current_temperature = 0
        self.old_temperature = 100
        
        self.fan_running = False
        
        self.sleep_time = 10
        self.DEBUG = debug
        
    def setup_gpio(self):
        if not self.pwm:
            self.pwm = RPi_PWM(self.PIN_FAN, self.FREQUENCY, self.PWM_MIN, self.PWM_MAX, self.PWM_MIN)
   
    
    def run (self):
        while self.fan_running:
            self.current_temperature = get_temp() # current temperature
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
            # not running
            if not self.pwm.is_running() and self.current_temperature > self.TEMP_START:
                self.pwm.start(self.PWM_MIN)   # starts at min speed
                print (f"{current_time} - fan started")
        
            if self.pwm.is_running():
                if self.old_temperature < self.current_temperature:
                    self.pwm.cycle += 5
                    
                elif self.current_temperature < self.old_temperature:
                    self.pwm.cycle -= 1
                    
                else:
                    self.pwm.cycle += 1
        
                # stop on low temp
                if self.current_temperature <= self.TEMP_STOP:
                    self.pwm.stop()
                    print (f"{current_time} - fan stopped")
            
            if self.DEBUG:
                print (f"{current_time} - temp: {self.current_temperature:.4f}, pwm: {self.pwm.cycle}, fan running: {self.pwm.is_running()}")
                
            self.old_temperature = self.current_temperature
            time.sleep(self.sleep_time)
        
        print (f"{current_time} - fan stopped")
        self.stop()

    def start(self):
        if not self.fan_running:
            self.setup_gpio()
            self.fan_running = True
            self.run()

    def stop(self):
        if self.fan_running:
            self.fan_running = False
            self.pwm.stop()

    def is_service_running(self):
        return self.fan_running
    
    def is_fan_running(self):
        return self.pwm.is_running()

    def get_current_temperature(self):
        return get_temp()          

    def get_current_pwm_signal(self):
        if self.pwm.cycle:
            return self.pwm.cycle
        else:
            return -1
        
    def get_start_temperature(self):
        return self.TEMP_START
    
    def get_stop_temperature(self):
        return self.TEMP_STOP
    
    def get_min_pwm(self):
        return self.pwm.min_cycle
    
    def get_max_pwm(self):
        return self.pwm.max_cycle
    
    def get_start_pwm(self):
        return self.pwm.start_cycle
    
    
    def set_start_temperature(self, temp):
        try:
            value = float(temp)
            self.TEMP_START = value
            
        except:
            pass
    
    def set_stop_temperature(self, temp):
        try:
            value = float(temp)
            self.TEMP_STOP = value
            
        except:
            pass
    
    def set_min_pwm(self, sig):
        try:
            value = int(sig)
            self.pwm.min_pwm = value
            
        except:
            pass
    
    def set_max_pwm(self, sig):
        try:
            value = int(sig)
            self.pwm.max_pwm = value
            
        except:
            pass
    
    def set_start_pwm(self, sig):
        try:
            value = int(sig)
            self.pwm.start_pwm = value
            
        except:
            pass
    
    
        
    def terminate(self):
        self.pwm.terminate()


