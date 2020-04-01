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

# update aws region and dynamodb table name from variables
sed -i -e "s/specify_aws_region/$AWS_REGION/" latest.py
sed -i -e "s/specify_dynamodb_table/$DYNAMODB_TABLE/" latest.py

# update dash auth user and password
sed -i -e "s/test_usr/$DASH_USR/" file.py
sed -i -e "s/test_pwd/$DASH_PWD/" file.py

# activate script flask venv, install flask app requirements and run wsgi server
/bin/bash -c ". /opt/pms3003/flask/bin/activate; python3 -m pip install -r requirements.txt; gunicorn --timeout 60 --bind 0.0.0.0:80 wsgi:application &"

# test in windows env
#waitress-serve wsgi:application
