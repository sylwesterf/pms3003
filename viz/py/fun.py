# -*- coding: utf-8 -*-
#!/bin/python
import boto3
import pandas as pd
import plotly.graph_objs as go

def dynamo_scan(table):
	
	# initial scan and data wrangling
	response = table.scan(table)
	data = response['Items']

	# create a pandas dataframe, wrangle the data
	df = pd.DataFrame(data, columns=['dt','pm1','pm25','pm10','temp','hum']).sort_values('dt').set_index('dt')
	df.index = pd.to_datetime(df.index)
	df['info'] = df.apply(lambda x: '' if pd.isnull(x['temp']) else ('temp: ' + str(int(x['temp'])) + '°C | hum: ' + str(int(x['hum'])) + '%'), axis=1)
	
	return df

def generate_graph(table):

	# get a dataframe
	df = dynamo_scan(table)

	# trace0 - pm1
	trace0 = go.Scatter(
		x=df.index,
		y=df['pm1'],
		name='pm1',
		mode= 'lines',
		visible='legendonly'
	)
	
	# trace1 - pm2.5
	trace1 = go.Scatter(
		x=df.index,
		y=df['pm25'],
		name='pm2.5',
		mode= 'lines'
	)
	
	# trace2 - pm10
	trace2 = go.Scatter(
		x=df.index,
		y=df['pm10'],
		name='pm10',
		text=df['info'],
		mode= 'lines'
		
	)
	
	# combine lines
	data = [trace0, trace1, trace2]
	
	layout = go.Layout(yaxis = dict(title = "µg/m3"),
				  xaxis=dict(
					rangeselector=dict(
					    buttons=list([
						dict(count=6,
						     label='6h',
						     step='hour',
						     stepmode='backward'),
						dict(count=1,
						     label='1d',
						     step='day',
						     stepmode='backward'),
						dict(count=7,
						     label='1w',
						     step='day',
						     stepmode='backward'),
						dict(count=14,
						     label='2w',
						     step='day',
						     stepmode='backward'),
						dict(step='all')
					    ])
					),
					rangeslider=dict(
					    visible = True
					),
					type='date'
				),
			   	shapes = [{
		    			'type': 'line',
		    			'x0': df.index[0],
		    			'y0': 4,
		    			'x1': df.index[-1],
		    			'y1': 4,
		    			'line': {
						'color': 'rgb(50, 171, 96)',
						'width': 4
		    			},
				}]

			)
	
	# get last update dt
	lastdt = str(df.index[-1])
	
	# get last measurements of pm25 and pm10
	lastpm = df[['pm25', 'pm10']].iloc[-1]

	# return quasi-live data
	return {'data': data, 'layout': layout, 'lastdt': lastdt, 'lastpm': lastpm}
