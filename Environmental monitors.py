from influxdb import InfluxDBClient
from time import localtime, strftime
import time
import smbus
import serial
bus=smbus.SMBus(1)
meas='Assembly_out'  #InfluxDB measurement name.
ifuser = "grafana"
ifpass = "bnlphysics"
ifdb   = "enviro_mon"
ifhost = "10.2.236.116"
ifport = 8086


ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

sample=60   #Sample Time in Seconds.
t_cor=.88   #Temperature correction, enclosure compensation.
AQM=0       #To activate AQM read, change to AQM=1.
smlprt=0    #Written as values to InfluxDB if AQM=0
lgprt=0
    
if AQM==1:
    port = serial.Serial("/dev/ttyUSB0")

RUN=True


while RUN:
    print(strftime("%H:%M:%S", localtime()))
    tis=int(time.time())
    ttis=0
    
    #Get data from SHT85 on i2c address 44 with temperature in degrees C and humidity in %.
    bus.write_byte_data(0x44, 0x24, 0x00)
    time.sleep(.5)
    data=bus.read_i2c_block_data(0x44, 0x00, 6)
    time.sleep(.5)
    t_data=data[0]<<8|data[1]
    h_data=data[3]<<8|data[4]
    
    temp=(-45.+175.*t_data/(2**16.))*t_cor
    temp_pr=float('%.3f'%temp)   #Set precision to 3.
    relh=100.*h_data/(2**16.)
    relh_pr=float('%.3f'%relh)
    
    #Get data from Pressure Sensor i2c address 28 with pressure in PSI.
    lvP=bus.read_i2c_block_data(0x28, 0x00, 4)
    press=(((lvP[0] & 63) << 8) | lvP[1]) * 30.0 / 16383.0
    press_pr=float('%.3f'%press)     #Set precision to 3.
    
    #Get data from Altimeter i2c address 60 with temp in degrees C and pressure in inHg.
    bus.write_byte_data(0x60, 0x26, 0x39)
    time.sleep(.5)
    l_p = bus.read_i2c_block_data(0x60, 0x00, 6)
    time.sleep(.5)
    b_press = (((((l_p[1] * 65536) + (l_p[2] * 256) + (l_p[3] & 0xF0)) / 16) / 4.0) / 1000.0)*0.295333727
    temp2 = ((((l_p[4]*256)+(l_p[5] & 0xF0))/16)/16)*t_cor
    b_press_pr=float('%.3f'%b_press)       #Set precision to 3.
    temp2_pr=float('%.3f'%temp2)
    
    #Get data from Dylos DC1100 Pro, Small and Large Particles in particles/cubic foot.
    if AQM==1:
        airqual=port.readline()
        print(airqual)
        realdata=eval(airqual)   #Converts byte data from DC1100 to integers.
        smlprt=realdata[0]
        lgprt=realdata[1]

    #Write measurements to InfluxDB database = home_enviro_mon to name specified in meas.
    field={'Temp[C]': temp_pr, 'Temp2[C]': temp2_pr,
                                              'Hum[%]': relh_pr, 'Press[PSI]':press_pr,
                                              'Press[inHg]': b_press_pr,
                                             'SmPrt[CF/100]': smlprt, 'LgPrt[CF/100]': lgprt}
    
    body = [
        {
            "measurement": meas,
            "time": time.time_ns(),
            
            "fields": field
        }
    ]
    
    ifclient.write_points(body)
    #60sec. timer between reads.
    while ttis <= 30:
        ctis=int(time.time())
        ttis=ctis-tis
    
    print(ttis)
    print()
    print("Temperature =", temp_pr, "C")
    print("Temperature2 =", temp2_pr, "C")
    print("Humidity =", relh_pr, "%")
    print("Pressure =", press_pr, "PSI")
    print("Pressure2 =",b_press_pr, "inHg")
    print("Small Particles=",smlprt, "CubFt/100")
    print("Large Particles=",lgprt, "CubFt/100")      
    
