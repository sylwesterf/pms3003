#!/bin/python
import time
import boto3
import csv
from pms3003 import PMSensor

# first run aws configure and set AWS Access Key ID and AWS Secret Access Key
# AWS STS or user with DynamoDB write Policy

# perform a data load

# call a PMSensor class
# 0 for indoor sensing, 1 for outdoor
pm = PMSensor(1)
	
# get PM1, PM2.5, PM10 values
pm1, pm25, pm10 = pm.read_pm()

# get time
pm_date = (time.strftime('%Y-%m-%d ') + time.strftime('%H:%M:%S'))

# write to csv
with open('pm-archive.csv','a+') as f:
 writer = csv.writer(f)
 writer.writerow([pm_date,pm1,pm25,pm10])

# write to dynamodb table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pms3003')

try:
	# insert the data
	table.put_item(
		Item={
		'dt' : pm_date,
		'pm1' : pm1,
		'pm25' : pm25,
		'pm10' : pm10
	    }
	)
	
except Exception:
	# write to csv in case of error
	with open('pm-not-loaded.csv','a+') as fn:
	 writer = csv.writer(fn)
	 writer.writerow([pm_date,pm1,pm25,pm10])

# sending SNS notification about new load
#client = boto3.client('sns')
#client.publish(
#    TopicArn = os.environ['loaded'],
#    Message = pm_date
#)
