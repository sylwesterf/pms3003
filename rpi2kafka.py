#!/bin/python
import time
from time import sleep
import numpy as np
from pms3003 import PMSensor
import RPi.GPIO as GPIO
import dht11
from kafka import KafkaProducer

# run aws configure and set AWS Access Key ID and AWS Secret Access Key

# set up kafka server 
kafka_server = 'xyz'
kafka_username = 'xyz'
kafka_password = 'xyz'
    
# topic to write to
topic = 'pms3003'

# instantiate producer
producer = KafkaProducer(
    bootstrap_servers=kafka_server,
    sasl_plain_username=kafka_username,
    sasl_plain_password=kafka_password,
    security_protocol = 'SASL_SSL',
    sasl_mechanism = 'SCRAM-SHA-256'
)

# run in an infinite loop
while 1:

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
    pm = PMSensor(1)

    # wakeup sensor and put into active mode if necessary
    #pm.write_serial('BM\xe4\x00\x01\x01t', 5)
    #pm.write_serial('BM\xe1\x00\x01\x01q', 5)

    # get PM1, PM2.5, PM10 values
    pm1, pm25, pm10 = pm.single_read() #verify if need to open/close port; update class potentially

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
    producer.send(topic, value=str(msg))
    sleep(5)
