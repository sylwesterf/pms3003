# Air quality monitoring station 
![lang](https://img.shields.io/github/languages/top/sylwesterf/pms3003.svg?style=flat)
![size](https://img.shields.io/github/repo-size/sylwesterf/pms3003.svg?style=flat)
![lastdt](https://img.shields.io/github/last-commit/sylwesterf/pms3003.svg?style=flat)
![rls](https://img.shields.io/github/release-date-pre/sylwesterf/pms3003.svg?style=flat)

This project consists of two parts:
- air quality monitoring station based of Raspberry Pi Zero W and PMS3003 sensor
- solution for measurement collection (AWS MySQL/DynamoDB) and data visualization (Plotly/Chart.js/R Shiny/Flask hosted on S3/EC2)

https://sylwester.cf/</br>
http://sylwesterf.s3-website.eu-central-1.amazonaws.com/</br>
https://sylwesterf.github.io/

## Installation

Raspberry Pi:

```sh
# download project files
sudo git clone https://github.com/sylwesterf/pms3003.git

# install dependencies
sudo pip install -r requirements.txt
# run aws configure and set AWS Access Key ID and AWS Secret Access Key

# enable uart
sudo echo "enable_uart=1" >> /boot/config.txt

# run a test
sudo python test.py

# fix paths in rpi2dynamodb.py and variables in csv2s3.py
```

EC2 - Flask:

```sh
# just add below commands to EC2 user data when launching an instance or ssh into it and run it afterwards
curl https://raw.githubusercontent.com/sylwesterf/pms3003/master/viz/py/prep.sh -o prep.sh
sudo bash prep.sh
rm prep.sh
```

## TODO
- add temperature and humidity sensor
- ~~create a javascript viz~~

## Acknowledgments
- https://github.com/Thomas-Tsai/pms3003-g3
- https://medium.com/@rfreeman/serverless-dynamic-real-time-dashboard-with-aws-dynamodb-a1a7f8d3bc01
- https://github.com/szazo/DHT11_Python

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
