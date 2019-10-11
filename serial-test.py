#!bin/python
import serial

test = serial.Serial('/dev/ttyS0', 9600, xonxoff=True)

#sleep
test.write('BM\xe4\x00\x00\x01s')
#wakeup
test.write('BM\xe4\x00\x01\x01t') 
#passive
test.write('BM\xe1\x00\x00\x01p')
#read in passive
test.write('BM\xe2\x00\x00\x01q')
#active
test.write('BM\xe1\x00\x01\x01q')

