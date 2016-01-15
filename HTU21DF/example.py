#!/usr/bin/python
"""
Testing the HTU21DF library.
"""

import time
from HTU21DF import HTU21DF

def main():
	address = 0x40

	print "Starting the HTU21DF..."

	htu = HTU21DF(address)

	# start = htu.begin()
	# print start
	if htu.begin():
		print "Success!!!"
		while True:
			#read_data(htu)
			print htu.readTemperature()
			time.sleep(0.5)
	else:
		print "The device is not running!!!"
	
		

def read_data(htu):
	while True:	

		print "The temperature is %f C." %(htu.readTemperature())
		time.sleep(1)
		
		print "The humidity is %F percent." %(htu.readHumidity())
		time.sleep(1)


if __name__ == '__main__':
	main()