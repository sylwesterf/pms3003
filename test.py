#!/bin/python
from pms3003 import PMSensor

# run to get particle measures in the console

# call a PMSensor class
# 0 for indoor sensing, 1 for outdoor
pm = PMSensor(0)
	
# print PM1, PM2.5, PM10 values
print(pm.read_pm())
