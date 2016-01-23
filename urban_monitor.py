import csv, os.path
import RPi.GPIO as GPIO
from BME280 import BME280
from ShinyeiPPD42 import Shinyei
from TSL2561 import TSL2561

def write_csv(data):
	fname = './data.csv'

	with open(fname, 'a') as f:
		w = csv.DictWriter(f, data.keys())
		w.writerow(data)

	f.close()

def main():
	GPIO.setmode(GPIO.BCM)
	
	bme = BME280()			# initialize bme280
	tsl = TSL2561()			# initialize tsl2561
	shinyei = Shinyei(18)	# initialize shinyei on gpio pin
	    
	while True:    
		aq = shinyei.read(30)				# I believe this is a blocking module

		degrees = bme.read_temperature()
		pascals = bme.read_pressure()
		hectopascals = pascals / 100
		humidity = bme.read_humidity()
		lux = tsl.lux()

		data = {
			'Time' : time.time(),
			'Temp' : bme.read_pressure(),
			'Pressure' : bme.read_pressure() / 100,
			'Humidity' : bme.read_humidity(),
			'Lux' : tsl.lux(),
			'LPO' : aq[0],
			'Ratio' : aq[1],
			'Concentration' : aq[2],
		}

		write_csv(data)
		print data

if __name__ == '__main__':
	main()
	GPIO.cleanup()	    