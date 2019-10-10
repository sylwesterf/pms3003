# -*- coding: utf-8 -*-
#!/bin/python
import os
from flask import Flask
from flask import send_from_directory

# initiate a flask app
pms3003 = Flask(__name__, static_folder='assets')

@pms3003.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(pms3003.root_path, 'assets'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@pms3003.route('/')
def index():
    return """
<!DOCTYPE html>
<head>
    <title>PMS3003</title>
</head>
<body>  
    <h2>Air quality monitoring station: </h2>
    <ul>
        <li><a href="https://github.com/sylwesterf/pms3003">Github repo</a></li>
        <li><a href="https://sylwesterf.github.io/">Chart.js implementation on Github webpages</a></li>
        <li><a href="http://sylwesterf.s3-website.eu-central-1.amazonaws.com">plotly.js implementation on S3</a></li>
        <li>Flask deployment on EC2: 
            <ul>
            <li>Last 50 days of data: <a href="/latest">/latest</a></li>
            <li>All data: <a href="/all">/all</a></li>
            </ul>
        </li>
    </ul>
</body>
"""