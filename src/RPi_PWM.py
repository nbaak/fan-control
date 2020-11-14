
import RPi.GPIO as GPIO

class RPi_PWM:
    
    def __init__(self, pin, frequency = 100, min_c= 0, max_c = 100, start_c = 100, mode = GPIO.BCM):
        self.pin = pin
        self.frequency = frequency
        
        self.pulsing = False    # not running initialy
        
        GPIO.setmode(mode)                  # mode; BCM = Board Mode
        GPIO.setwarnings(False)             # gpio warnings
        GPIO.setup(self.pin, GPIO.OUT)      # set pwm pin to output
        
        self.pwm = GPIO.PWM(self.pin, self.frequency)
              
        self.min_cycle = min_c
        self.start_cycle = start_c
        self.max_cycle = max_c
        
        self.cycle = 0
        
    
    @property
    def cycle(self):
        return self.__cycle
    
    @cycle.setter
    def cycle(self, cycle):
        if cycle > self.max_cycle:
            self.__cycle = self.max_cycle
        elif cycle < self.min_cycle:
            self.__cycle = self.min_cycle
        else:
            self.__cycle = cycle
            
        if self.is_running():
            self.update_pwm_signal()
        
    
    def start(self, cycle = 0):
        if not self.is_running():
            self.cycle = cycle
            self.pwm.start(self.start_cycle) 
            self.pwm.ChangeFrequency(self.frequency)
            self.pulsing = True
        
    def stop(self):
        if self.is_running():
            self.pwm.stop()
            self.pulsing = False
            
    def update_pwm_signal(self):
        if self.is_running():
            self.pwm.ChangeDutyCycle(self.cycle)
    
    def set_frequency(self, frequency):
        self.frequency = frequency
        
    def set_min_cycle(self, cycle):
        self.min_cycle = cycle
        
    def set_max_cycle(self, cycle):
        self.max_cycle = cycle
    
    def set_start_cycle(self, cycle):
        self.start_cycle = cycle
        
    def is_running(self):
        return self.pulsing
    
    
    def terminate(self):
        self.stop()
        GPIO.cleanup()
        