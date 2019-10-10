#!/usr/bin/env bash

# define flask app directory
flaskdir="/opt/pms3003/"

# install nginx and git
yum install nginx, git -y
amazon-linux-extras install nginx1.12 -y

# install python3
yum install python3 -y
pip3 install --upgrade pip

# install virtualenv for isolated Python environment
python3 -m pip install virtualenv

# create flask virtual environment
mkdir $flaskdir && cd $flaskdir
/usr/local/bin/virtualenv flask

# get code from github
git clone https://github.com/sylwesterf/pms3003.git

# copy viz files
cp -r pms3003/viz/py-new/* .

# activate script flask venv, install flask app requirements and run wsgi server
/bin/bash -c ". /opt/pms3003/flask/bin/activate; pip install -r requirements.txt; gunicorn --bind 0.0.0.0:80 wsgi:application &"


