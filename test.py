#!/bin/python
from pms3003 import PMSensor
import RPi.GPIO as GPIO
import dht11

# run to get particle measures in the console

# set up variables
device = '/dev/serial0'
environment = 1

# call a PMSensor class
pm = PMSensor(device, environment)
	
# print avg'ed PM1, PM2.5, PM10 values
print(pm.read_pm())

# wakeup pms3003 (if necessary) and print a single read
#pm.write_serial(b'BM\xe4\x00\x01\x01t', 45)
#pm.write_serial(b'BM\xe1\x00\x01\x01q', 15)
#print(pm.single_read())

# setup dht11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read dth11 data using pin 4
instance = dht11.DHT11(pin = 4)
while True:
    result = instance.read()
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)
    break
	
GPIO.cleanup()
