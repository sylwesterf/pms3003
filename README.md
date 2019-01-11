# Air quality monitoring station 

This project consists of two parts:
- air quality monitoring station based of Raspberry Pi Zero W and PMS3003 sensor
- solution for measurement collection and data visualization (MySQL/DynamoDB + R Shiny/Flask)

## Installation

On Raspberry Pi:

```sh
# download project files
sudo git clone https://github.com/sylwesterf/pms3003.git

# get pip
#curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#python get-pip.py
#rm -f get-pip.py

# install dependencies for mysql or dynamodb
sudo pip install -r mysql/requirements.txt
# OR
sudo pip install -r dynamodb/requirements.txt

# enable uart
$ sudo echo "enable_uart=1" >> /boot/config.txt
```
