#!/bin/python
import time
import boto3
import csv
import numpy as np
from pms3003 import PMSensor

# set up project path for csv generation
path = '/project/path/'

# set sensor environment - indoor/outdoor (0/1)
environment = 1

# set up gpio serial port
# /dev/ttyAMA0 -> Bluetooth (or GPIO when Bluetooth module turned off)
# /dev/ttyS0 -> GPIO serial port (also referenced as '/dev/serial0')
device = '/dev/serial0' 

# set up dynamodb table name
dynamodb_table = 'pms3003'

# call a PMSensor class
pm = PMSensor(device, environment)

# get PM1, PM2.5, PM10 values
data = pm.read_pm()

# reject outliers
data = data[np.all(np.abs((data - np.mean(data, axis=0))) <= 2 * np.std(data, axis=0), axis=1)]
data = data[np.array(data[:,2], dtype=float)/np.array(data[:,1], dtype=float) < 2]
data = data[np.array(data[:,2], dtype=float) > np.array(data[:,1], dtype=float)]

# get the pm average as an int
pm1, pm25, pm10 = np.mean(data, axis=0, dtype=int)

# get current timestamp
pm_date = (time.strftime('%Y-%m-%d ') + time.strftime('%H:%M:%S'))

# write to csv
with open(path + 'pm-archive.csv','a+') as f:
 writer = csv.writer(f)
 writer.writerow([pm_date,pm1,pm25,pm10])

# write to dynamodb table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table)

try:
        # insert the data
        table.put_item(
                Item={
                'device' : 'pms3003',
                'dt' : pm_date,
                'pm1' : str(pm1),
                'pm25' : str(pm25),
                'pm10' : str(pm10)
                }
        )

except Exception:
        # write to csv in case of error
        with open(path + 'pm-not-loaded.csv','a+') as fn:
         writer = csv.writer(fn)
         writer.writerow([pm_date,pm1,pm25,pm10])
		
	# SNS notification about an unsuccessful load
        #sns = boto3.resource('sns')
        #topic = sns.Topic('arn::pastehere::')
        #response = topic.publish(
        #       Message='Problem loading data on: ' + pm_date,
        #       Subject='PMS3003 Unsuccessful Data Load',
        #       MessageStructure='string'
        #)
