#!/usr/bin/env python
import time as t
import datetime
from sht85 import sht85
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "grafana"
ifpass = "bnlphysics"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "sht85data"

#define shtobject
shtsensor= sht85(1)


while True:
    # take a timestamp for this measurement
    time = datetime.datetime.utcnow()

    # collect some stats from shtsensor
    shtdata = shtsensor.get_data()
    shttemp = shtdata[0]
    shthum  = shtdata[1]
#    shthumidity = shtsensor.get_humidity()

    # format the data as a single measurement for influx
    body = [
        {
            "measurement": measurement_name,
            "time": time,
            
            "fields": {
                "temp": shttemp,
                "humidity": shthum,
            }
        }
    ]

    # connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

    # write the measurement
    ifclient.write_points(body)
    t.sleep(1)