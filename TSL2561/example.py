#!/usr/bin/python
"""
Testing the TSL2561 library.
"""

import time
from TSL2561 import TSL2561

def main():
	
	print "Starting the TSL2561..."

	tsl = TSL2561(debug=1)
	
	while True:
		print tsl.lux()
		time.sleep(0.5)


if __name__ == '__main__':
	main()