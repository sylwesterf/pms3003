#!/usr/bin/env bash

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

# create directories
mkdir $flaskdir && cd $flaskdir

# install export-dynamodb for dynamodb dumps
python3 -m pip install export-dynamodb

# set default region
aws configure set default.region eu-central-1

# install cron job
printf "# cron job for dynamodb table dump into csv\n6 0 * * * /usr/local/bin/export-dynamodb -t pms3003 -f csv -o /opt/pms3003/output.csv > /dev/null 2>&1\n" > cron.txt
crontab /opt/pms3003/cron.txt

# create flask virtual environment
/usr/local/bin/virtualenv flask

# get code from github
git clone https://github.com/sylwesterf/pms3003.git

# copy viz files
cp -r pms3003/viz/py-new/* .

# activate script flask venv, install flask app requirements and run wsgi server
/bin/bash -c ". /opt/pms3003/flask/bin/activate; python3 -m pip install -r requirements.txt; gunicorn --bind 0.0.0.0:80 wsgi:application &"


