#!bin/python
import serial

test = serial.Serial('/dev/serial0', 9600, xonxoff=True)

#sleep
test.write(b'BM\xe4\x00\x00\x01s')
#wakeup
test.write(b'BM\xe4\x00\x01\x01t') 
#passive
test.write(b'BM\xe1\x00\x00\x01p')
#read in passive
test.write(b'BM\xe2\x00\x00\x01q')
#active
test.write(b'BM\xe1\x00\x01\x01q')

