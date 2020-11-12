import smbus

class tmp102:
    @staticmethod
    def get_temperature():
        resolution = 0.0625
        bus = smbus.SMBus(1)
        data = bus.read_i2c_block_data(0x48,0)
        msb = data[0]
        lsb = data[1]
        
        #bit shifting
        fullWord = (((msb << 8) | lsb) >> 4)

        # negative temperatures
        if msb & 0x80: 
            fullWord = fullWord | (-1 - 0x7ff)
        
        # ggf this.resolution, muss getestet werden
        temperature = int(fullWord) * resolution
        return temperature
