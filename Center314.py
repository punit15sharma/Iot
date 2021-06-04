import serial
from serial import *
import time


class Center_314:
    def __init__(self,location="/dev/ttyUSB0",timeout=1):
        self.humi=serial.Serial(location,9600,EIGHTBITS,parity=PARITY_NONE,stopbits=STOPBITS_ONE,timeout=1)
    
    
    def read(self):
        self.humi.write( ("A" + '\r\n').encode() )
        byteline = self.humi.read(10)
        strLine = byteline.hex()
        humval = int(strLine[6:10], 16) / 10 
        t1val = int(strLine[10:14],16)/10
        #t2val = int(strLine[14:18],16)/10
        ret={"humidity_Cen": humval,"temp_Cen":t1val}
        return ret


if __name__=="__main__":
    humi=Center_314()
    print(humi.read())
