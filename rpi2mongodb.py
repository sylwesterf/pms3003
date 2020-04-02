#!/bin/python
import time
from time import sleep
import numpy as np
from pms3003 import PMSensor
import RPi.GPIO as GPIO
import dht11
import pymongo

# set sensor environment - indoor/outdoor (0/1)
environment = 1

# set up gpio serial port
# /dev/ttyAMA0 -> Bluetooth (or GPIO when Bluetooth module turned off)
# /dev/ttyS0 -> GPIO serial port (also referenced as '/dev/serial0')
device = '/dev/serial0' 

# set up mongo db variables
mongo_server = "xyz:27017"
mongo_db = "xyz"
mongo_col = "xyz"

# instantiate mongodb client
client = pymongo.MongoClient("mongodb://" + mongo_server)
db = client[mongo_db]
col = db[mongo_col]

last_pm1, last_pm25, last_pm10 = 0, 0, 0

# run in an infinite loop
while True:

    # get dht11 data
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    #GPIO.cleanup()

    # read dht11 data using pin 4
    instance = dht11.DHT11(pin = 4)		#verify if pin is correct

    # loop over to get a valid result
    while True:
        result = instance.read()
        if result.is_valid():
            temp, hum = [result.temperature, result.humidity]
            break

    # GPIO cleanup
    GPIO.cleanup()

    # call a PMSensor class
    # 0 for indoor sensing, 1 for outdoor
    pm = PMSensor(device, environment)

    # wakeup sensor and put into active mode if necessary
    #pm.write_serial('BM\xe4\x00\x01\x01t', 5)
    #pm.write_serial('BM\xe1\x00\x01\x01q', 5)

    # get PM1, PM2.5, PM10 values
    pm1, pm25, pm10 = pm.single_read()
    
    # data checks
    if pm1 >= pm25 or pm25 >= pm10:
        pm1, pm25, pm10 = last_pm1, last_pm25, last_pm10
    elif pm25 != 0 and last_pm25 != 0 and (last_pm25 * 3 <= pm25 or pm25 <= last_pm25 * 0.3):
        pm1, pm25, pm10 = last_pm1, last_pm25, last_pm10

    last_pm1, last_pm25, last_pm10 = pm1, pm25, pm10

    # get current timestamp
    pm_date = (time.strftime('%Y-%m-%d ') + time.strftime('%H:%M:%S'))

    # define a message
    msg = {
     'device' : 'pms3003',
     'dt' : pm_date,
     'pm1' : pm1,
     'pm25' : pm25,
     'pm10' : pm10,
     'temp' : temp,
     'hum' : hum,
    }

    # send data
    col.insert_one(msg)
    sleep(1)
