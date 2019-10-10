# -*- coding: utf-8 -*-
#!/bin/python
import boto3
import dash
import dash_auth
import dash_html_components as html
from fun import serve_layout_all
from pwd import pwd

# get the service resource
dynamodb = boto3.resource('dynamodb', region_name = 'eu-central-1')

# instantiate a table resource object 
table = dynamodb.Table('pms3003')

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/all_pms3003/'
)

# authentication
auth = dash_auth.BasicAuth(
    app,
    pwd
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

# call layout function 
app.layout = serve_layout_all(table)