#!/bin/python
import time
import boto3
import csv
import numpy as np
from pms3003 import PMSensor
import RPi.GPIO as GPIO
import dht11

# first run aws configure and set AWS Access Key ID and AWS Secret Access Key

# call a PMSensor class
# 0 for indoor sensing, 1 for outdoor
pm = PMSensor(1)
	
# get PM1, PM2.5, PM10 values
data = pm.read_pm()

# reject outliers
data = data[np.all(np.abs((data - np.mean(data, axis=0))) < 2 * np.std(data, axis=0), axis=1)]
data = data[np.array(data[:,2], dtype=float)/np.array(data[:,1], dtype=float) < 2]

# get the average as an int
pm1, pm25, pm10 = np.mean(data, axis=0, dtype=int)

# get dht11 data
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read dth11 data using pin 7
instance = dht11.DHT11(pin = 7)
result = instance.read()
temp, hum = result.temperature, result.humidity

# get current timestamp
pm_date = (time.strftime('%Y-%m-%d ') + time.strftime('%H:%M:%S'))

# write to csv
with open('/path/to/csv/file/pm-archive.csv','a+') as f:
 writer = csv.writer(f)
 writer.writerow([pm_date,pm1,pm25,pm10,temp,hum])

# write to dynamodb table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pms3003')
#table_raw = dynamodb.Table('pms3003raw')

try:
	# insert the data
	table.put_item(
		Item={
		'dt' : pm_date,
		'pm1' : pm1,
		'pm25' : pm25,
		'pm10' : pm10,
		'temp' : temp,
		'hum' : hum
	    }
	)
	
	# insert raw data
        #for i in range(data.shape[0]):
        #        table_raw.put_item(
        #                Item={
        #                'dt' : pm_date[:15] + "0 " + str(i),
        #                'pm1' : data[i,0],
        #                'pm25' : data[i,1],
        #                'pm10' : data[i,2]
        #            }
        #        )
		
	# sending SNS notification about new load
	#sns = boto3.resource('sns')
	#topic = sns.Topic('arn::pastehere::')
	#response = topic.publish(
    	#	Message='Data was successfully loaded on: ' + pm_date,
    	#	Subject='PMS3003 Data Load',
    	#	MessageStructure='string'
	#)
	
except Exception:
	# write to csv in case of error
	with open('/path/to/csv/file/pm-not-loaded.csv','a+') as fn:
	 writer = csv.writer(fn)
	 writer.writerow([pm_date,pm1,pm25,pm10,temp,hum])
