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
		visible='legendonly',
		line=dict(color="#1f77b4", width=2)
	)
	
	# trace1 - pm2.5
	trace1 = go.Scatter(
		x=df.index,
		y=df['pm25'],
		name='pm2.5',
		mode= 'lines',
		line=dict(color="#2ca02c", width=2)
	)
	
	# trace2 - pm10
	trace2 = go.Scatter(
		x=df.index,
		y=df['pm10'],
		name='pm10',
		text=df['info'],
		mode='lines',
		line=dict(color="#ff7f0e", width=2)
		
	)
	
	# get last update dt
	lastdt = str(df.index[-1])
	
	# get first dt
	firstdt = str(df.index[0])
	
	# combine lines
	data = [trace0, trace1, trace2]
	
	layout = go.Layout(yaxis = dict(title = "µg/m3", 
				gridcolor = "#eeeeee", 
				zerolinecolor = "#444444"),
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
					type='date',
					gridcolor = "#eeeeee", 
					zerolinecolor = "#444444"
				  ),
			plot_bgcolor = "#ffffff",
			paper_bgcolor	= "#ffffff",
			shapes = [dict(
					type = "line",
					layer = "above",
					line = dict(
						color = "#cf0101",
						width = 2
					),
					y0 = 25,
					y1 = 25,
					x0 = generate_graph(table)['firstdt'],
					x1 = generate_graph(table)['lastdt']
					)],
			annotations=[dict(
					x=generate_graph(table)['lastdt'],
					y=25,
					xref="x",
					yref="y",
					text="PM2.5 = 25"
					)]
			)

	
	# get last measurements of pm25 and pm10
	lastpm = df[['pm25', 'pm10']].iloc[-1]

	# return quasi-live data
	return {'data': data, 'layout': layout, 'firstdt': firstdt, 'lastdt': lastdt, 'lastpm': lastpm}
