from BME280 import BME280
from ShinyeiPPD42 import Shinyei
from TSL2561 import TSL2561

def main():
	sensor = BME280(mode=BME280_OSAMPLE_8)
    tsl = TSL2561()
	GPIO.setmode(GPIO.BCM)
	shinyei = Shinyei(18)
    	    
    while True:    
        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        hectopascals = pascals / 100
        humidity = sensor.read_humidity()
        lux = tsl.lux()
        shinyei.read(30)

        print 'Timestamp = {0:0.3f}'.format(sensor.t_fine)
        print 'Temp      = {0:0.3f} deg C'.format(degrees)
        print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
        print 'Humidity  = {0:0.2f} %'.format(humidity)
        print 'Lux       = {0} %}'.format(lux)
        time.sleep(5)	

if __name__ == '__main__':
	main()
	GPIO.cleanup()	    