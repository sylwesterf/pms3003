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
    return "Main page"