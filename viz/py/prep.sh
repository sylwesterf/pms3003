#!/usr/bin/env bash
# input variables: 
# $1    $AWS_REGION 
# $2    $DYNAMODB_TABLE

# define flask app directory
flaskdir="/opt/pms3003/"

# install nginx and git
yum install nginx, git -y
amazon-linux-extras install nginx1.12 -y

# install python3
yum install python3 -y
python3 -m pip install --upgrade pip

# install virtualenv for isolated Python environment
python3 -m pip install virtualenv

# create flask virtual environment
mkdir $flaskdir && cd $flaskdir
virtualenv flask

# get code from github
git clone https://github.com/sylwesterf/pms3003.git

# copy viz files
cp pms3003/viz/py/{fun.py,requirements.txt,vizflask.py,wsgi.py} .
cp -a pms3003/viz/py/assets .

# update aws region and dynamodb table name from variables
sed -i -e "s/specify_aws_region/$1/" latest.py
sed -i -e "s/specify_dynamodb_table/$2/" latest.py

# activate script flask venv, install flask app requirements and run wsgi server
/bin/bash -c ". /opt/pms3003/flask/bin/activate; python3 -m pip install -r requirements.txt; gunicorn --bind 0.0.0.0:80 wsgi:server &"
