#!/bin/python
import boto3
import pandas as pd

# write to dynamodb table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pms3003')
table_js = dynamodb.Table('pms3003js')

# function for scan
def dynamo_scan(table):
 response = table.scan(table)
 data = response['Items']
 df = pd.DataFrame(data, columns=['dt','pm1','pm25','pm10']).sort_values('dt').set_index('dt').astype(int)
 df.index = pd.to_datetime(df.index)
 return df

# scan the table
df = dynamo_scan(table)

# loop over and put items with sort index
for i in range(df.shape[0]):
        table_js.put_item(
                Item={
				'device' : 'pms3003',
                'dt' : str(df.index[i]),
                'pm1' : df.pm1[i],
                'pm25' : df.pm25[i],
                'pm10' : df.pm10[i]
            }
        )
