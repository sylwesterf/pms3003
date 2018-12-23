#!/bin/bash
yum update -y
curl https://raw.githubusercontent.com/sylwesterf/pms3003/master/viz/py/prep.sh -o prep.sh
sudo bash prep.sh
rm prep.sh
