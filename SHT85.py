import time
import smbus
#from Sensors.Sensor import Sensor

class sht85():
    def __init__(self,bus=3,address=0x44):
        self.bus=smbus.SMBus(int(bus))
        self.address=address
        

    def get_data(self):
        #Write the read sensor command
        self.bus.write_byte_data(self.address, 0x24, 0x00)
        time.sleep(0.1) #This is so the sensor has tme to preform the mesurement and write its registers before you read it

        # Read data back, 8 bytes, temperature MSB first then lsb, Then skip the checksum bit then humidity MSB the lsb.
        data0 = self.bus.read_i2c_block_data(self.address, 0x00, 8)

        t_val = (data0[0]<<8) + data0[1] #convert the data

        h_val = (data0[3] <<8) + data0[4]     # Convert the data
        T = ((175.72 * t_val) / 65536.0 ) - 45 #do the maths from datasheet
        H = ((100 * h_val) / 65536.0 )
        return [T,H]

    def get_temperature(self):
        return self.get_data["temperature"]

    def get_humidity(self):
        return self.get_data['humidity']
    
