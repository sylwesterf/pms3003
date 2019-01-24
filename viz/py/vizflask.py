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
from fun import dynamo_scan, generate_graph

# get the service resource
dynamodb = boto3.resource('dynamodb', region_name = 'eu-central-1')

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

app.title = 'PMS3003'

# function for app layout call
def serve_layout():
    
    # dash app layout definition
    serve = html.Div(style={'backgroundColor': colors['background']}, children=[

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
            id = 'live-graph',
            animate = False,
            figure = go.Figure(
                data = generate_graph(table)['data'],
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
						dict(count=1,
						     label='1m',
						     step='month',
						     stepmode='backward'),
						dict(step='all')
					    ])
					),
					rangeslider=dict(
					    visible = True
					),
					type='date'
				 )
				  )
            )
        ),
            
        # last updated date
        html.Div(id='update-date', children = generate_graph(table)['lastdt'], style={
            'textAlign': 'right',
            'color': colors['text'],
            'fontSize': 12
        }),
	    
	# latest results pm10
        html.Div(id='update-pm10', children = 'PM10: ' + str(generate_graph(table)['lastpm']['pm10']), style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 80,
	    'marginTop': 5,
	    'marginLeft': 24,
        }),
	    
	# latest results pm25
        html.Div(id='update-pm25', children = 'PM2.5: ' + str(generate_graph(table)['lastpm']['pm25']), style={
            'textAlign': 'left',
            'color': colors['text'],
            'fontSize': 80,
	    'marginTop': 8,
	    'marginLeft': 24,
        }),

        # event update handler
        dcc.Interval(
                id='event-update',
                interval=20*1*1000
        )
    ])

    return serve

# call layout function - enables data refresh on page refresh
app.layout = serve_layout

# app callback for graph update
@app.callback(Output('live-graph', 'data'),
              events=[Event('event-update', 'interval')])
			  
# function for the graph udpate
def update_graph():
    
	# re-scan the table
	return generate_graph(table)

# app callback for lastdt update
@app.callback(Output('update-date', 'children'),
		events=[Event('event-update', 'interval')])

# function for lastdt update
def update_date():
	
	# re-scan the table and get last update dt
	lastdt = generate_graph(table)['lastdt']
	return lastdt

# app callback for pm10 update
@app.callback(Output('update-pm10', 'children'),
		events=[Event('event-update', 'interval')])

# function for latest results
def update_pm10():
	
	# re-scan the table and get last update dt
	lastpm = generate_graph(table)['lastpm']
	lastpm10 = 'PM10: ' + str(lastpm['pm10'])
	return lastpm10

# app callback for pm25 update
@app.callback(Output('update-pm25', 'children'),
		events=[Event('event-update', 'interval')])

# function for latest results
def update_pm25():
	
	# re-scan the table and get last update dt
	lastpm = generate_graph(table)['lastpm']
	lastpm25 = 'PM25: ' + str(lastpm['pm25'])
	return lastpm25


# run
#if __name__ == '__main__':
#    app.run_server(host="0.0.0.0", port=80)
