# The MIT License (MIT)

# Copyright (c) 2016 Nicholas Johnson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# The following code reads multiple sensor inputs and writes the data to a
# csv file.  BME280, TSL2561 are connected via I2C and the ShinyeiPPD42 is
# connected to a digital GPIO pin.

import csv, os.path
import RPi.GPIO as GPIO
import time
from BME280 import BME280
from ShinyeiPPD42 import Shinyei
from TSL2561 import TSL2561

__author__ = "Nicholas Johnson <nejohnson2@gmail.com>"
__copyright__ = "Copyright (C) 2004 Nicholas Johnson"
__license__ = "MIT"
__version__ = "v1.0"

'''History
v1.0 - First Release
'''

def write_csv(data):
	'''Write data to a csv file'''
	fname = './data.csv'

	with open(fname, 'a') as f:
		w = csv.DictWriter(f, data.keys())
		w.writerow(data)

	f.close()

def main():
	'''Main program loop'''
	
	# Initialize sensors
	try:
		bme = BME280()
	except:
		print "Failed to load the BME280 sensor"
		exit()
	try:
		tsl = TSL2561()
	except:
		print "Failed to load the TSL2561 sensor"
		exit()
	try:
		shinyei = Shinyei(18)
	except:
		print "Failed to initialize the Shinyei sensor"
		exit()
	    
	while True:    
		# Read data from the shinyei sensor.  I believe
		# this is a blocking module so the loop will only 
		# not run while the shinyei is reading.
		aq = shinyei.read(30)				

		# Read the rest of the sensors
		data = {
			'Time' : time.time(),
			'Temp' : bme.read_temperature(),
			'Pressure' : bme.read_pressure() / 100, # divide by 100 to get hetopascals hPa
			'Humidity' : bme.read_humidity(),
			'Lux' : tsl.lux(),
			'LPO' : aq[0],
			'Ratio' : aq[1],
			'Concentration' : aq[2],
		}

		# write data to csv
		write_csv(data)

		print data

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	main()
	GPIO.cleanup()	    