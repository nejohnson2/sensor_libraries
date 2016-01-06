#!/usr/bin/python
"""
Testing the HTU21DF library.
"""

import time
import HTU21DF

def main():
	address = 0x40

	print "Starting the HTU21DF..."

	htu = HTU21DF(address)

	while True:
		if htu.begin():
			read_data(htu)
		
		time.sleep(0.5)

def read_data(htu):
	while True:	

		print "The temperature is %f C." %(htu.read_temperature())
		time.sleep(1)
		
		print "The humidity is %F percent." %(htu.read_humidity())
		time.sleep(1)


if __name__ == '__main__':
	main()