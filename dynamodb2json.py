#!/bin/python
import boto3
import pandas as pd
import datetime
from boto3.dynamodb.conditions import Attr

# read from dynamodb
dynamodb = boto3.resource('dynamodb', region_name = 'region')

# instantiate a table resource object 
table = dynamodb.Table('table_name')

# get 3 days of data
dt_offset = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
response = table.scan(
					FilterExpression=Attr('dt').gt(dt_offset) 
					)
data = response['Items']

# create a pandas dataframe
df = pd.DataFrame(data, columns=['dt','pm1','pm25','pm10']).sort_values('dt').set_index('dt').astype(int)
df = df.reset_index()

# convert to json
df_json = df.to_json(orient='records')

# upload json file to s3
s3 = boto3.resource('s3')
obj = s3.Object('bucket_name','file.json')
response = obj.put(Body=df_json)

# update ACLs
obj_acl = s3.ObjectAcl('bucket_name','file.json')
response = obj_acl.put(ACL='public-read')
