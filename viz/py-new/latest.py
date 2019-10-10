# -*- coding: utf-8 -*-
#!/bin/python
import boto3
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event, Input
import plotly.graph_objs as go
from fun import generate_graph, serve_layout_subset
import datetime
from datetime import timedelta

# get the service resource
dynamodb = boto3.resource('dynamodb', region_name = 'eu-central-1')

# instantiate a table resource object 
table = dynamodb.Table('pms3003')

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/latest/'
)

# html head section
app.title = 'PMS3003'
app.config.suppress_callback_exceptions = True

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <link rel='shortcut icon' type='image/x-icon' href='/assets/favicon.ico' />
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
    </body>
</html>
'''

# call layout function - enables data refresh on page refresh
app.layout = serve_layout_subset(table)

# set date filter
dt_limit = str(datetime.datetime.now() - datetime.timedelta(days=50))
    
# app callback for graph update
@app.callback(Output('live-graph', 'figure'),
              events=[Event('event-update', 'interval')])
			  
# function for the graph udpate
def update_graph():
    
	# re-scan the table
	return generate_graph(table, dt_limit)

# app callback for header update
@app.callback(Output('update-header', 'children'),
		events=[Event('event-update', 'interval')])

# function for header update
def update_header():
	
	# re-scan the table and get last update dt
	lastdt = 'Data as of: ' + generate_graph(table, dt_limit)['lastdt'][11:13] + '.' + generate_graph(table, dt_limit)['lastdt'][14:15] + '0:'
	return lastdt

# app callback for pm10 update
@app.callback(Output('update-pm10', 'children'),
		events=[Event('event-update', 'interval')])

# function for latest results
def update_pm10():
	
	# re-scan the table and get last update dt
	lastpm = generate_graph(table, dt_limit)['lastpm']
	lastpm10 = 'PM10: ' + str(lastpm['pm10']) + ' (' +  str(generate_graph(table, dt_limit)['lastpm']['pm10'] * 2) + '%)'
	return lastpm10

# app callback for pm25 update
@app.callback(Output('update-pm25', 'children'),
		events=[Event('event-update', 'interval')])

# function for latest results
def update_pm25():
	
	# re-scan the table and get last update dt
	lastpm = generate_graph(table, dt_limit)['lastpm']
	lastpm25 = 'PM2.5: ' + str(lastpm['pm25']) + ' (' +  str(generate_graph(table, dt_limit)['lastpm']['pm25'] * 4) + '%)'
	return lastpm25

# app callback for lastdt update
@app.callback(Output('update-date', 'children'),
		events=[Event('event-update', 'interval')])

# function for lastdt update
def update_date():
	
	# re-scan the table and get last update dt
	lastdt = 'Last update: ' + generate_graph(table, dt_limit)['lastdt']
	return lastdt 