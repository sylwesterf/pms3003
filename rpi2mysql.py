#!/bin/python
import time
import sys
import mysql.connector
from mysql.connector import errorcode
from pms3003 import PMSensor

# set sensor environment - indoor/outdoor (0/1)
environment = 1

# set up gpio serial port
# /dev/ttyAMA0 -> Bluetooth (or GPIO when Bluetooth module turned off)
# /dev/ttyS0 -> GPIO serial port (also referenced as '/dev/serial0')
device = '/dev/serial0' 

# create a connection string
cnx_string = "mysql.connector.connect(host='xxx', port=3306, user='rpi', password='xxx')"

# connect to mysql
try:
	cnx = eval(cnx_string)
except mysql.connector.Error as e:
	sys.exit(1)

# create a cursor
cur = cnx.cursor()

# perform a data load

# call a PMSensor class
# 0 for indoor sensing, 1 for outdoor
pm = PMSensor(device, environment)
	
# get PM1, PM2.5, PM10 values
pm1, pm25, pm10 = pm.read_pm()

# get time
pm_date = (time.strftime('%Y-%m-%d ') + time.strftime('%H:%M:%S'))

# insert statement
sql = ("""INSERT INTO db_pms3003.fct_pm (pm1, pm25, pm10, dt) VALUES (%s,%s,%s,%s)""",(pm1, pm25, pm10, pm_date))

try:	
	# execute insert 
	cur.execute(*sql)
	
	# commit insert
	cnx.commit()
	
except Exception:
	# rollback in case of error
	cnx.rollback()

cur.close()
cnx.close()
