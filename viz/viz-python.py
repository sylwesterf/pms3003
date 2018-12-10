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

df.plot()

#2

import plotly.plotly as py
import plotly.graph_objs as go

trace0 = go.Scatter(
    x=df.index,
    y=df['pm1'],
    name='pm1'
)
trace1 = go.Scatter(
    x=df.index,
    y=df['pm25'],
    name='pm2.5'
)
trace2 = go.Scatter(
    x=df.index,
    y=df['pm10'],
    name='pm10'
)

data = [trace0, trace1, trace2]

import plotly
plotly.tools.set_credentials_file(username='xyz', api_key='xyz')
py.iplot(data)

#3
import plotly
import plotly.graph_objs as go

plotly.offline.init_notebook_mode(connected=True)

plotly.offline.iplot({
    "data": data,
    "layout": go.Layout(title="Zanieczyszczenie powietrza", yaxis = dict(title = "µg/m3"))
})
