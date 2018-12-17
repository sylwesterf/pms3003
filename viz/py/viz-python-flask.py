# -*- coding: utf-8 -*-
#!/bin/python
import flask
import time
import pandas as pd
import boto3
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event
import plotly
import plotly.graph_objs as go

# get the service resource
dynamodb = boto3.resource('dynamodb')

# instantiate a table resource object 
table = dynamodb.Table('pms3003')

# initiate a dash app
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

# set formatting
colors = {
    'background': '#ffffff',
    'text': '#111101'
}

# actual dash app layout definition
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

	# title
    html.H1(
        children='Zanieczyszczenie powietrza',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
	
	# graph
    dcc.Graph(
        id='live-graph',
		animate = True
    ),
	
	# graph update handler, every 15mins
	dcc.Interval(
            id='graph-update',
            interval=900*1000	
        ),
		
	# last updated note
	html.Div(id='update-date', style={
        'textAlign': 'right',
        'color': colors['text'],
		'fontSize': 12
    })
])

# app callback for graph update
@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
			  
# function for the graph udpate
def update_graph():

	# scan the table
	response = table.scan()
	data = response['Items']
	
	# create a pandas dataframe, wrangle the data
	df = pd.DataFrame(data, columns=['dt','pm1','pm25','pm10']).sort_values('dt').set_index('dt').astype(int)
	df.index = pd.to_datetime(df.index)

	# trace0 - pm1
	trace0 = plotly.graph_objs.Scatter(
		x=df.index,
		y=df['pm1'],
		name='pm1',
		mode= 'lines+markers'
	)
	
	# trace1 - pm2.5
	trace1 = plotly.graph_objs.Scatter(
		x=df.index,
		y=df['pm25'],
		name='pm2.5',
		mode= 'lines+markers'
	)
	
	# trace2 - pm10
	trace2 = plotly.graph_objs.Scatter(
		x=df.index,
		y=df['pm10'],
		name='pm10',
		mode= 'lines+markers'
	)
	
	# combine lines
	data = [trace0, trace1, trace2]

	# return quasi-live data for graph's figure attribute
	return {'data': data,'layout' : go.Layout(yaxis = dict(title = "µg/m3")),'children':'testat'}

@app.callback(Output('update-date', 'children'),
			  events=[Event('graph-update', 'interval')])

def update_date():
	
	# scan the table
	response = table.scan()
	data = response['Items']
	lastdt = 'Ostatni pomiar wykonano ' + str(data[0]['dt'])
		
	return lastdt
	
# run
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=80)
