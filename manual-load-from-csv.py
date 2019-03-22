#!/bin/python
import pandas as pd
import boto3
import time
import os

# read values that weren't loaded into dynamodb
df = pd.read_csv('pm-not-loaded.csv')

# set up dynamodb client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pms3003')

# write to a dynamodb table
for i in range(df.shape[0]):
        table.put_item(
                Item={
                'dt' : df.dt[i],
                'pm1' : int(df.pm1[i]),
                'pm25' : int(df.pm25[i]),
                'pm10' : int(df.pm10[i]),
                'temp' : float(df.temp[i]),
                'hum' : float(df.hum[i])
            }
        )

# set up variables for s3 upload		
s3filename = time.strftime('manual-load-%Y-%m-%d.csv')
s3bucket = 's3bucket'
filename = '/path/to/csv/file/pm-not-loaded.csv'

# create an S3 client
s3 = boto3.client('s3')

# upload csv
s3.upload_file(filename, s3bucket, s3filename)

os.remove(filename)
