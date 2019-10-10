# -*- coding: utf-8 -*-
#!/bin/python
import boto3
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from boto3.dynamodb.conditions import Key, Attr
import datetime
from datetime import timedelta

# set formatting
colors = {
    'background': '#ffffff',
    'text': '#111101'
}

def dynamo_scan(table, filter=0):
    
    # initial scan and data wrangling
    if filter == 0:
        response = table.scan()
    else:
        response = table.scan(FilterExpression=Attr('dt').gt(filter))	
    
    data = response['Items']
    
    # create a pandas dataframe, wrangle the data
    df = pd.DataFrame(data, columns=['dt','pm1','pm25','pm10','temp','hum']).sort_values('dt').set_index('dt')
    df.index = pd.to_datetime(df.index)
    df['info'] = df.apply(lambda x: '' if pd.isnull(x['temp']) else ('temp: ' + str(int(x['temp'])) + '°C | hum: ' + str(int(x['hum'])) + '%'), axis=1)

    return df

def csv_scan(file):
    
    # read csv, create a pandas dataframe and wrange the data
    df = pd.read_csv("output.csv")[['dt','pm1','pm25','pm10','temp','hum']].sort_values('dt').set_index('dt')
    df.index = pd.to_datetime(df.index)
    df['info'] = df.apply(lambda x: '' if pd.isnull(x['temp']) else ('temp: ' + str(int(x['temp'])) + '°C | hum: ' + str(int(x['hum'])) + '%'), axis=1)

    return df

def generate_graph_all(file):

	# get a dataframe
	df = csv_scan(file)

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
		visible='legendonly',
		line=dict(color="#ff7f0e", width=2)
	)

	# trace 3 - PM2.5 limit line
	trace3 = go.Scatter(
		x=df.index,
		y=[25]*df.shape[0],
		name='PM2.5 = 25 µg/m3',
		mode='lines',
		line=dict(color="#cf0101", width=2),
		hoverinfo='none'
	)

	# trace 4 - PM10 limit line
	trace4 = go.Scatter(
		x=df.index,
		y=[50]*df.shape[0],
		name='PM10 = 50 µg/m3',
		mode='lines',
		line=dict(color="#cf0101", width=2),
		visible='legendonly',
		hoverinfo='none'
	)
	
	# combine lines
	data = [trace0, trace1, trace2, trace3, trace4]

	# create plotly layout
	layout = go.Layout(yaxis = dict(title = "µg/m3", 
				gridcolor = "#eeeeee", 
				zerolinecolor = "#444444"),
			xaxis=dict(
					rangeselector=dict(
						buttons=list([
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
						dict(count=1,
							label='1m',
							step='month',
							stepmode='backward'),
						dict(count=3,
							label='3m',
							step='month',
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
			paper_bgcolor	= "#ffffff"
			)

	# return quasi-live data
	return {'data': data, 'layout': layout}
	
def generate_graph(table, filter=0):

	# get a dataframe
	df = dynamo_scan(table, filter)

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
		visible='legendonly',
		line=dict(color="#ff7f0e", width=2)
	)
	
	# get last update dt
	lastdt = str(df.index[-1])
	
	# get first dt
	firstdt = str(df.index[0])
	
	# combine lines
	data = [trace0, trace1, trace2]

	# get PM2.5 limit line
	if filter == 0:
		shapes = []
		annotations = []

		trace3 = go.Scatter(
			x=df.index,
			y=[25]*df.shape[0],
			name='PM2.5 = 25 µg/m3',
			mode='lines',
			line=dict(color="#cf0101", width=2),
			hoverinfo='none'
		)
		trace4 = go.Scatter(
			x=df.index,
			y=[50]*df.shape[0],
			name='PM10 = 50 µg/m3',
			mode='lines',
			line=dict(color="#cf0101", width=2),
			visible='legendonly',
			hoverinfo='none'
		)
		data.extend([trace3, trace4])
	else:
		shapes = [dict(
						type = "line",
						layer = "above",
						line = dict(
							color = "#cf0101",
							width = 2
						),
						y0 = 25,
						y1 = 25,
						x0 = firstdt,
						x1 = lastdt
						)]

		annotations=[dict(
						x=str(df.index[-130]),
						y=25,
						showarrow=True,
						xref="x",
						yref="y",
						ay=-100, 
						ax=-100,
						text="PM2.5 = 25"
						)]
	
	# create plotly layout
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
			shapes = shapes,
			annotations=annotations
			)
	
	
	# get last measurements 
	lastpm = df[['pm25', 'pm10', 'pm1', 'temp', 'hum']].iloc[-1]

	# return quasi-live data
	return {'data': data, 'layout': layout, 'firstdt': firstdt, 'lastdt': lastdt, 'lastpm': lastpm}

def serve_layout_subset():
    
    # get the service resource
    dynamodb = boto3.resource('dynamodb', region_name = 'eu-central-1')

    # instantiate a table resource object 
    table = dynamodb.Table('pms3003')

	# set date filter
    dt_limit = str(datetime.datetime.now() - datetime.timedelta(days=50))
    
    # dash app layout definition
    layout = html.Div(style={'backgroundColor': colors['background']}, children=[

        # title
        html.H1(
            children='Air Pollution',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        # graph
        dcc.Graph(
            id = 'live-graph',
            animate = False,
            figure = go.Figure(
                data = generate_graph(table, dt_limit)['data'],
                layout = generate_graph(table, dt_limit)['layout']
            )
        ),

        # header pm
        html.Div(id='update-header', children = 'Data as of: ' + generate_graph(table, dt_limit)['lastdt'][11:13] + '.' + generate_graph(table, dt_limit)['lastdt'][14:15] + '0:', style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 27,
	    'marginTop': 2,
	    'marginLeft': 24
        }),
	    
		# latest results pm10
        html.Div(id='update-pm10', children = 'PM10: ' + str(generate_graph(table, dt_limit)['lastpm']['pm10']) 
		 + ' (' +  str(generate_graph(table, dt_limit)['lastpm']['pm10'] * 2) + '%)', style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 27,
	    'marginTop': 5,
	    'marginLeft': 24
        }),
	    
		# latest results pm25
        html.Div(id='update-pm25', children = 'PM2.5: ' + str(generate_graph(table, dt_limit)['lastpm']['pm25'])
		  + ' (' +  str(generate_graph(table, dt_limit)['lastpm']['pm25'] * 4) + '%)', style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 27,
	    'marginTop': 5,
	    'marginLeft': 24
        }),

		# latest results pm1
        html.Div(id='update-pm1', children = 'PM1: ' + str(generate_graph(table, dt_limit)['lastpm']['pm1']), style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 27,
	    'marginTop': 5,
	    'marginLeft': 24
        }),

		# latest results humidity
        html.Div(id='update-hum', children = 'Humidity: ' + str(generate_graph(table, dt_limit)['lastpm']['hum'])
		  + '%', style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 18,
	    'marginTop': 5,
	    'marginLeft': 24
        }),

		# latest results temp
        html.Div(id='update-temp', children = 'Temperature: ' + str(generate_graph(table, dt_limit)['lastpm']['temp'])
		  + '°C', style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 18,
	    'marginTop': 5,
	    'marginLeft': 24
        }),
	    
		# last updated date
        html.Div(id='update-date', children = 'Last update: ' + generate_graph(table, dt_limit)['lastdt'], style={
            'textAlign': 'right',
            'color': colors['text'],
            'fontSize': 9
        }),

        # event update handler
        dcc.Interval(
                id='event-update',
                interval=60*4*1000	# update every 4 minutes
        )
    ])

    return layout

def serve_layout_all():
    
	# set filename
    file = "output.csv"
    
    # dash app layout definition
    layout = html.Div(style={'backgroundColor': colors['background']}, children=[

        # title
        html.H1(
            children='Air Pollution',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        
        # graph
        dcc.Graph(
            id = 'live-graph',
            animate = False,
            figure = go.Figure(
                data = generate_graph_all(file)['data'],
                layout = generate_graph_all(file)['layout']
            )
        )
    ])

    return layout