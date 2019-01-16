#!/bin/python
import boto3
import time
import os

# update variables for upload
s3filename = time.strftime('%Y/%m/%d.csv')
s3bucket = 's3bucket'
filename = '/path/to/csv/file/pm-archive.csv'

try:
	
	# create an S3 client
	s3 = boto3.client('s3')
	
	# upload today's archive csv
	s3.upload_file(filename, s3bucket, s3filename)
	
	# remove archive csv from host
	os.remove(filename)
	
except Exception:
	pass
