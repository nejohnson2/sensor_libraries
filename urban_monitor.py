import RPi.GPIO as GPIO
from BME280 import BME280
from ShinyeiPPD42 import Shinyei
from TSL2561 import TSL2561

def main():
	GPIO.setmode(GPIO.BCM)

	sensor = BME280()
	tsl = TSL2561()
	shinyei = Shinyei(18)	# add pin number
	    
	while True:    
		shinyei.read(30)						# I believe this is a blocking module

		degrees = sensor.read_temperature()
		pascals = sensor.read_pressure()
		hectopascals = pascals / 100
		humidity = sensor.read_humidity()

		lux = tsl.lux()

		print 'Timestamp = {0:0.3f}'.format(sensor.t_fine)
		print 'Temp      = {0:0.3f} deg C'.format(degrees)
		print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
		print 'Humidity  = {0:0.2f} %'.format(humidity)
		print 'Lux       = {0} %}'.format(lux)
		#print 'Particles per 0.01 cubic feet:'

if __name__ == '__main__':
	main()
	GPIO.cleanup()	    