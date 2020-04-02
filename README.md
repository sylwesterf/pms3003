# Air quality monitoring station 
![lang](https://img.shields.io/github/languages/top/sylwesterf/pms3003.svg?style=flat)
![size](https://img.shields.io/github/repo-size/sylwesterf/pms3003.svg?style=flat)
![lastdt](https://img.shields.io/github/last-commit/sylwesterf/pms3003.svg?style=flat)
![rls](https://img.shields.io/github/release-date-pre/sylwesterf/pms3003.svg?style=flat)
![lic](https://img.shields.io/github/license/sylwesterf/pms3003.svg)

This project consists of three parts:
1. Air quality monitoring station based of Raspberry Pi Zero W and PMS3003 sensor
2. Data transfer and storage (MySQL/DynamoDB/S3/MongoDB/Kafka) 
3. Data visualization (Plotly/Chart.js/R Shiny/Flask hosted on S3/EC2/github.io)

https://sylwester.cf/</br>
http://sylwesterf.s3-website.eu-central-1.amazonaws.com/</br>
https://sylwesterf.github.io/

## Installation
#### 1. Air quality monitoring station

Clone github repository to your Raspberry Pi Zero W and install dependencies.

```sh
# download project files
sudo git clone https://github.com/sylwesterf/pms3003.git
cd pms3003

# install dependencies
sudo pip3 install -r requirements.txt
```

Follow RaspberryPi documentation to enable uart: https://www.raspberrypi.org/documentation/configuration/uart.md

Connect PMS3003 to Raspberry Pi as per sensor datasheet:

| PMS3003       | Rpi           |
|           --- |---            |
| VCC           | +5V           |
| GND           | GND           |
| RxD           | TxD           |
| TxD           | RxD           |


Connect DHT11 (3 PIN) to Raspberry Pi as per sensor datasheet:

| PMS3003       | Rpi           |
|           --- |---            |
| VCC           | +3.3V         |
| OUT           | GPIO7 (BCM)   |
| GND           | GND           |

Test the set up. Make sure you specify a correct path to gpio serial port for device variable (line 9) and select appropriate value for environment variable (line 10) - 0/1 for a sensor placed outdoor/indoor respectively. Use *serial-test.py* (scripts folder) to troubleshoot issues with serial port configuration.

```sh
# run a test - output to terminal
sudo python test.py
```

#### 2. Data transfer and storage

##### DynamoDB

In order to use AWS DynamoDB as a storage option you need to set up programmatic access for your Raspberry Pi (use AWS CLI) and edit *rpi2dynamodb.py* file (modify variables accordingly):
- path - a project path used for backup csv generation (line 11)
- environment - sensor environment:  0/1 for a sensor placed outdoor/indoor respectively (line 14)
- device - gpio serial port (line 18)
- dynamodb_table - DynamoDB table to write data to (line 22)

Note: AWS IAM user should have write priviliges for DynamoDB and S3.

```sh
# run aws configure and set AWS Access Key ID and AWS Secret Access Key for DynamoDB/S3 upload
sudo aws configure

# run rpi2dynamodb.py script to load data into DynamoDB and generate a (backup) csv file on Raspberry Pi
sudo python3 rpi2dynamodb.py
#sudo python3 rpi2dynamodb_onlypm.py
```

A *csv2s3.py* file can be used to upload CSVs (generated by *rpi2dynamodb.py*) into S3. Two variables need to be updated: 
- s3bucket - AWS S3 bucket name (line 8)
- filename - CVS filename inculding its path (line 9)

```sh
# automatic archival of csv files into S3
sudo python csv2s3.py
```

Upon successful testing a cronjob can be set up:
- to measure the air quality hourly and sent data into DynamoDB table,
- to archive csv files into S3 at the end of the day.

##### MySQL

To store air quality data in MySQL a fct_pm table needs to be created first and necessary permissions set (update mysql user password):

```sql
CREATE TABLE db_pms3003.fct_pm
(
pm1 int NOT NULL,
pm25 int NOT NULL,
pm10 int NOT NULL,
dt datetime NOT NULL
);

CREATE USER 'rpi' IDENTIFIED BY 'xxx';
GRANT INSERT ON db_pms3003.fct_pm TO 'rpi';
```

Install packages on Raspberry Pi:
```sh
pip install mysql-connector-python
```

Update the following in *rpi2mysql.py* file:
- environment - sensor environment:  0/1 for a sensor placed outdoor/indoor respectively (line 9)
- device - gpio serial port (line 14)
- cnx_string - host and password for MySQL (line 17)

##### Apache Kafka

Install packages
```sh
pip install kafka-python
```

Update the following in *rpi2kafka.py* file:
- environment - sensor environment:  0/1 for a sensor placed outdoor/indoor respectively (line 11)
- device - gpio serial port (line 16)
- kafka_server (line 19)
- kafka_username (line 20)
- kafka_password (line 21)
- topic - kafka topic to write data to (line 24)

*rpi2kafka.py* is configured to send data (in an infinite loop) every 5 seconds.

##### MongoDB

Install packages
```sh
pip install pymongo
```

Update the following in *rpi2mongodb.py* file:
- environment - sensor environment:  0/1 for a sensor placed outdoor/indoor respectively (line 11)
- device - gpio serial port (line 16)
- mongo_server (line 19)
- mongo_db (line 20)
- mongo_col (line 21)

*rpi2mongodb.py* is configured to send data (in an infinite loop) every 1 second.

#### 3. Data visualization 

##### Flask - NEW (hosted on AWS EC2) 
Flask application assumes a DynamoDB table is created and populated using a solution described in DynamoDB section under 2. Data transfer and storage. </br>
Attach an IAM role to EC2 for DynamoDB Read and S3 Upload.</br>
Add commands below to EC2 user data when launching an instance or ssh into it and run it afterwards.</br>
Update variables AWS_REGION and DYNAMODB_TABLE with your AWS region and DynamoDB table name (see sample).</br>
You can also set DASH_USR and DASH_PWD variables that are going to be used to authenticate into one of the app routes - /all </br>

```sh
#!/bin/bash
export AWS_REGION=your_aws_region
export DYNAMODB_TABLE=your_dynamodb_table

# sample
#export AWS_REGION=eu-central-1
#export DYNAMODB_TABLE=pms3003

export DASH_USR=test_usr
export DASH_PWD=test_pwd

# prep script
sudo curl https://raw.githubusercontent.com/sylwesterf/pms3003/master/viz/py-new/prep.sh -o prep.sh
sudo bash prep.sh $AWS_REGION $DYNAMODB_TABLE $DASH_USR $DASH_PWD
sudo rm prep.sh
```

Flask app directory:
```sh
/opt/pms3003/
.
├── pms3003.py
├── latest.py
├── all.py
├── dockerfile
├── fun.py
├── assets/
│   └── favicon.ico
├── file.py
├── wsgi.py
├── prep.sh
├── output.csv
└── requirements.txt
```

##### Flask - Docker
Flask application assumes a DynamoDB table is created and populated using a solution described in DynamoDB section under 2. Data transfer and storage. </br>
Pull an image from DockerHub repo and run a container with setting environment variables for AWS Region, DynamoDB table name (default is *'pms3003'*) and number of days to display on graph (default is 21).

```sh
# install docker
sudo yum install docker -y
sudo systemctl start docker

# pull from dockerhub repo
sudo docker pull sylwesterf/pms3003:latest
sudo docker images -a

# run a container (attach an IAM role to EC2 for DynamoDB Read and S3 Upload)
sudo docker run -p 80:8000 -e AWS_REGION="xyz" -e DYNAMODB_TABLE="xyz" -e DT_FILTER=21 sylwesterf/pms3003:latest
#sudo docker run -p 80:8000 -e AWS_REGION="eu-central-1" -e DYNAMODB_TABLE="pms3003" -e DT_FILTER=6 sylwesterf/pms3003:latest
```

You can run the same container without an IAM role assumed by EC2 Instace, but by utilizing an IAM user with programmatic access and read permissions for DynamoDB. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables by providing them in docker's run command.

```sh
# run a container without assumed IAM role
sudo docker run -p 80:8000 -e AWS_ACCESS_KEY_ID="xyz" -e AWS_SECRET_ACCESS_KEY="xyz" -e DASH_USR="xyz" -e DASH_PWD="xyz" -e AWS_REGION="xyz" -e DYNAMODB_TABLE="xyz" DT_FILTER=21 sylwesterf/pms3003:latest
```

A dockerfile used to build the image is available under *viz\py\dockerfile*.
Follow below commands to create an image on your own by pulling and building from *viz/py*. folder from this repo.
```sh
sudo docker build https://github.com/sylwesterf/pms3003.git#master:viz/py --tag pms3003
sudo docker run -p 80:8000 -e AWS_REGION="xyz" -e DYNAMODB_TABLE="xyz" -e DT_FILTER=21 pms3003
```

##### Flask - OLD (hosted on AWS EC2) 
Flask application assumes a DynamoDB table is created and populated using a solution described in DynamoDB section under 2. Data transfer and storage. </br>
Attach an IAM role to EC2 for DynamoDB Read and S3 Upload.</br>
Add commands below to EC2 user data when launching an instance or ssh into it and run it afterwards.</br>
Update variables AWS_REGION and DYNAMODB_TABLE with your AWS region and DynamoDB table name (see sample).</br>

```sh
#!/bin/bash
export AWS_REGION=your_aws_region
export DYNAMODB_TABLE=your_dynamodb_table

# sample
#export AWS_REGION=eu-central-1
#export DYNAMODB_TABLE=pms3003

# prep script
sudo curl https://raw.githubusercontent.com/sylwesterf/pms3003/master/viz/py/prep.sh -o prep.sh
sudo bash prep.sh $AWS_REGION $DYNAMODB_TABLE
sudo rm prep.sh
```

Flask app directory:
```sh
/opt/pms3003/
.
├── fun.py
├── assets/
│   └── favicon.ico
├── wsgi.py
└── requirements.txt
```

##### R-Shiny
Shiny application assumes a MySQL table was created and populated using a solution described in MySQL section under 2. Data transfer and storage. </br>
Deploy the contents of *pms3003/viz/R/pms3003/* into your shiny server </br>
For shiny server setup on EC2 follow the *pms3003/viz/R/pms3003/ec2_ubuntu_config_R.sh* </br>
Create a 'shiny' user on MySQL server (update mysql user password).

```sql
CREATE USER 'shiny' IDENTIFIED BY 'xxx';
GRANT SELECT ON db_pms3003.fct_pm TO 'shiny';
```

##### Chart.js (hosted on github.io)
Deploy the contents of *pms3003/viz/js-chart/* into your github.io webpage. Update the url for json src file in *script.js* </br>
Make sure to enable CORS for S3 bucket as per: https://stackoverflow.com/questions/49493279/react-js-how-to-get-rid-of-cross-origin-error-in-codesandbox if you're sourcing a json file from S3 </br>
See https://sylwesterf.github.io/ and corresponding repo https://github.com/sylwesterf/sylwesterf.github.io

You can use AWS CLI to dump DynamoDB table into json file.
```sh
aws dynamodb scan --table-name TABLE_NAME > output.json
```
##### plotly.js (hosted on AWS S3) 
Upload the contents of *pms3003/viz/js-plotly/* into your S3 bucket and update the url for json src file in *script.js* </br>

You can clone this github repo, update the url for json src file in *script.js* and run below AWS CLI command from *pms3003/viz/js-plotly* directory (update your bucket name) to deploy the visualization:
```sh
aws s3 cp . s3://your_bucket_name/ --recursive
```

See http://sylwesterf.s3-website.eu-central-1.amazonaws.com

#### 4. Extras

Refer to *pms3003/scripts/* for helpful scripts: </br>
- dynamodb-update-table.py (add humidity and temperature data to DynamoDB table)
- dynamodb2json.py (export data to json format)
- index-reset-reload.py (move data from non-indexed to indexed table)
- manual-load-from-csv.py (perfrom a manual load from csv to DynamoDB)
- power-consumption.sh (reduce RasberryPi W power consumption)
- serial-test.py (test gpio port)
- rpi2dynamodb_onlypm.py (excludes dht11 data)

## TODO
- ~~temperature and humidity sensor to viz~~
- ~~a javascript viz~~
- ~~add PM2.5=25 limit threshold line~~
- ~~new layout~~
- case for sensors 
- ~~authentication~~
- ~~sending data to kafka~~
- ~~sending data to mongodb~~
- ~~contenerize viz~~
- ~~python 3~~
- lightweight distro for container (debian/alpine)

## Acknowledgments
- https://github.com/Thomas-Tsai/pms3003-g3
- https://medium.com/@rfreeman/serverless-dynamic-real-time-dashboard-with-aws-dynamodb-a1a7f8d3bc01
- https://github.com/szazo/DHT11_Python
- https://github.com/okomarov/dash_on_flask
- https://medium.com/@kmmanoj/deploying-a-scalable-flask-app-using-gunicorn-and-nginx-in-docker-part-1-3344f13c9649

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
