#!/bin/python
import time
import pandas as pd
import boto3

# select statement
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pms3003')

response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])

df = pd.DataFrame(data, columns=['dt','pm1','pm25','pm10']).sort_values('dt').set_index('dt').astype(int)
df.index = pd.to_datetime(df.index)
