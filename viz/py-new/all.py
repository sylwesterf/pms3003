# -*- coding: utf-8 -*-
#!/bin/python
import boto3
import dash
import dash_auth
import dash_html_components as html
from fun import serve_layout_all
from file import pwd

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/all/'
)

# authentication
auth = dash_auth.BasicAuth(
    app,
    pwd
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <title>PMS3003</title>
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
app.layout = serve_layout_all