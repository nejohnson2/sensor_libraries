import csv, os.path
import RPi.GPIO as GPIO
from BME280 import BME280
from ShinyeiPPD42 import Shinyei
from TSL2561 import TSL2561

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
	bme = BME280()
	tsl = TSL2561()
	shinyei = Shinyei(18)
	    
	while True:    
		# Read data from the shinyei sensor.  I believe
		# this is a blocking module so the loop will only 
		# not run while the shinyei is reading.
		aq = shinyei.read(30)				

		# Read the rest of the sensors
		data = {
			'Time' : time.time(),
			'Temp' : bme.read_pressure(),
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