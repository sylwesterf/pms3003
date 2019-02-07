#!bin/python
import serial
import time
import numpy as np

class PMSensor():
	
	def __init__(self, env):
	
		# hardcode the serial port
		self.port = '/dev/ttyS0'
		
		# sensor placed indoor/outdoor (0/1)
		self.standard = env
		
		# hardcode the baudrate
		self.baudrate = 9600
		
		# enable software flow control.
		self.xonxoff = True
		
		# timeout
		self.timeout = 30
		
		self.serial = None

	def open_port(self):
	
		# open serial port
		self.serial = serial.Serial(self.port, baudrate=self.baudrate, xonxoff=self.xonxoff, timeout=self.timeout)

	def fixed_bytes(self):
		
		while True:
		
			#get two starting bytes
			start_bytes = self.serial.readline(2)
			start_bytes_hex = start_bytes.encode('hex')
			
			#check for fixed characters
			if start_bytes_hex == '424d':
				return True 

	def read_serial(self):
		
		# read from uart, up to 22 bytes
		data_uart = self.serial.readline(22)
		
		# encode
		data_hex = data_uart.encode('hex')
		
		# calculate pm values
		# indoor
		if self.standard == 0:
			pm1  = int(data_hex[4] + data_hex[5] + data_hex[6] + data_hex[7], 16)
			pm25 = int(data_hex[8] + data_hex[9] + data_hex[10] + data_hex[11], 16)
			pm10 = int(data_hex[12] + data_hex[13] + data_hex[14] + data_hex[15], 16)
		# outdoor
		elif self.standard == 1:
			pm1  = int(data_hex[16] + data_hex[17] + data_hex[18] + data_hex[19], 16)
			pm25 = int(data_hex[20] + data_hex[21] + data_hex[22] + data_hex[23], 16)
			pm10 = int(data_hex[24] + data_hex[25] + data_hex[26] + data_hex[27], 16)
        
		# store values in a list
		values = [pm1, pm25, pm10]
        
		# close serial port
		self.serial.close()
		
		# return data
		return values

	def write_serial(self, cmd, timeout=0):
		
		# open serial port
		self.open_port()
		
		# writes binary data to the serial port
		write = self.serial.write(cmd)
		
		# set timeout
		time.sleep(timeout)

	def single_read(self):
		
		# open serial port
		self.open_port()
		
		while True:
			# the number of bytes in the input buffer should be non-zero to avoid errors
			if self.serial.inWaiting() > 0:
			
				# validate generated data
				if self.fixed_bytes() == True:
				
					# get the pm values
					data = self.read_serial()
				
				# data read-out
				return data
	
	def read_pm(self):
		
		# wakeup sensor with 45sec timeout
		self.write_serial('BM\xe4\x00\x01\x01t', 55)
		
		# put into active mode
		self.write_serial('BM\xe1\x00\x01\x01q', 15)
		
		# measure pm n-times
		n = 10
		data = self.single_read()
		for i in range(1,n):
			time.sleep(10)
			data = np.append([data], [self.single_read()])
			time.sleep(5)
		
		# reshape list into matrix
                data = data.reshape((n,3))
		
		# put the sensor in the passive mode
		self.write_serial('BM\xe1\x00\x00\x01p')
		
		# standby mode, aka. sleep
		self.write_serial('BM\xe4\x00\x00\x01s')
		
		# close serial port
		self.serial.close()
		
		# return averaged data
		return data
	
