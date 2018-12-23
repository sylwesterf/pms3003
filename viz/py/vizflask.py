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
dynamodb = boto3.resource('dynamodb', region = 'eu-central-1')

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
            animate = True,
            figure = go.Figure(
                data = generate_graph(table)['data'],
                layout = go.Layout(yaxis = dict(title = "µg/m3"))
            )
        ),
            
        # last updated date
        html.Div(id='update-date', children = generate_graph(table)['lastdt'], style={
            'textAlign': 'right',
            'color': colors['text'],
            'fontSize': 12
        }),

        # event update handler
        dcc.Interval(
                id='event-update',
                interval=4*1000
        )
    ])

    return serve

# call layout function - enables data refresh on page refresh
app.layout = serve_layout

# app callback for graph update
@app.callback(Output('live-graph', 'figure'),
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

# run
#if __name__ == '__main__':
#    app.run_server(host="0.0.0.0", port=80)
