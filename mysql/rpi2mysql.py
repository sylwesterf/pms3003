#!/bin/python
import time
import MySQLdb
from pms3003 import PMSensor

# configure MySQL
db = MySQLdb.connect(
	host='xxx',
	user='xxx',
	passwd='xxx',
	db='xxx',
	port=3306
)

# open a cursor
cur = db.cursor()

# perform a data load

# call a PMSensor class
# 0 for indoor sensing, 1 for outdoor
pm = PMSensor(1)
	
# get PM1, PM2.5, PM10 values
pm1, pm25, pm10 = pm.read_pm()

# get time
pm_date = (time.strftime('%Y-%m-%d ') + time.strftime('%H:%M:%S'))

# insert statement
sql = ("""INSERT INTO fct_pm (pm1, pm25, pm10, dt) VALUES (%s,%s,%s,%s)""",(pm1, pm25, pm10, pm_date))

try:	
	# execute insert 
	cur.execute(*sql)
	
	# commit insert
	db.commit()
	
except Exception:
	# rollback in case of error
	db.rollback()

cur.close()
db.close()
