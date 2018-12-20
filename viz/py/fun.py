#!/bin/python
import boto3
import pandas as pd
import plotly.graph_objs as go

def dynamo_scan(table):
	
	# initial scan and data wrangling
	response = table.scan(table)
	data = response['Items']

	# create a pandas dataframe, wrangle the data
	df = pd.DataFrame(data, columns=['dt','pm1','pm25','pm10']).sort_values('dt').set_index('dt').astype(int)
	df.index = pd.to_datetime(df.index)
	
	return df

def generate_graph(table):

	# get a dataframe
	df = dynamo_scan(table)

	# trace0 - pm1
	trace0 = go.Scatter(
		x=df.index,
		y=df['pm1'],
		name='pm1',
		mode= 'lines+markers'
	)
	
	# trace1 - pm2.5
	trace1 = go.Scatter(
		x=df.index,
		y=df['pm25'],
		name='pm2.5',
		mode= 'lines+markers'
	)
	
	# trace2 - pm10
	trace2 = go.Scatter(
		x=df.index,
		y=df['pm10'],
		name='pm10',
		mode= 'lines+markers'
	)
	
	# combine lines
	data = [trace0, trace1, trace2]
	
	# get last update dt
	lastdt = 'Ostatni pomiar wykonano ' + str(df.index[-1])

	# return quasi-live data for graph's figure attribute
	return {'data': data, 'lastdt': lastdt}
