# -*- coding: utf-8 -*-
import wiringpi
import os
import struct
from time import sleep
#import sqlite3
#import sys
#import time

wiringpi.wiringPiSetup() #setup wiringpi
i2c = wiringpi.I2C() #get I2C
dev = i2c.setup(0x40) #setup I2C device
i2c.write(dev,0x02) #HDC1000 CONFIGURATION POINTER
i2c.write(dev,0x10) #send 1byte
i2c.write(dev,0x00) #send 1byte
sleep((6350.0 + 6500.0 +  500.0)/1000000.0)
dataAry = struct.unpack("BBBB",os.read(dev,4))
os.close(dev)
temp = (dataAry[0] << 8) | (dataAry[1])
hudi = (dataAry[2] << 8) | (dataAry[3])
temp = ((temp / 65535.0) * 165 - 40)
hudi = ((hudi / 65535.0 ) * 100)
#print "Humidity %.2f" % hudi
#print "Temperature %.2f" % temp
print (temp, hudi)

#datetime = "%s" % (time.strftime("%Y/%m/%d %H:%M:%S"))

#dbname = sys.argv[1]
#conn = sqlite3.connect(dbname)
#cursor = conn.cursor()

#insert_str = "insert into temperature (unixtime, datetime, temperature, humidity) values (%s, \"%s\", %f, %f)" % (time.time(), datetime, temp, hudi)
#cursor.execute(insert_str)

#conn.commit()
#cursor.close()
#conn.close()

