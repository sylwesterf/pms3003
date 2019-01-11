# Air quality monitoring station 

This project consists of two parts:
- air quality monitoring station based of Raspberry Pi Zero W and PMS3003 sensor
- solution for measurement collection and data visualization (AWS MySQL/DynamoDB + R Shiny/Flask hosted on EC2)

## Installation

Raspberry Pi:

```sh
# download project files
sudo git clone https://github.com/sylwesterf/pms3003.git

# install dependencies for dynamodb
sudo pip install -r requirements.txt
# run aws configure and set AWS Access Key ID and AWS Secret Access Key

# enable uart
sudo echo "enable_uart=1" >> /boot/config.txt

# run a test
sudo python test.py
```

EC2 - Flask:

```sh
# just add below commands to EC2 user data when launching an instance or ssh into it and run it afterwards
curl https://raw.githubusercontent.com/sylwesterf/pms3003/master/viz/py/prep.sh -o prep.sh
sudo bash prep.sh
rm prep.sh
```

## Acknowledgments
- https://github.com/Thomas-Tsai/pms3003-g3
