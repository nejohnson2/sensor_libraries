import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta

class pm:
	def __init__(self, pin):
		self.sampletime_ms = 30000
		self.lowpulseoccupancy = 0
		self.concentration = 0
		self.ratio = 0
		self.gpio = pin 

	def read(self):
		"""
		Not sure if this is correct!
		"""
		GPIO.setup(self.gpio, GPIO.IN)
		return GPIO.input(self.gpio)

	def calc_particles(self):
		self.ratio = self.lowpulseoccupancy / (self.sampletime_ms * 10.0); # Integer percentage 0=>100
		self.concentration = 1.1 * pow(self.ratio, 3) - 3.8 * pow(self.ratio, 2) + 520 * self.ratio + 0.62; #using spec sheet curve
		
		print "LPO : %s  -  Ratio : %s  -  Concentration : %s" %(self.lowpulseoccupancy, self.ratio, self.concentration)

		self.lowpulseoccupancy = 0
		

def main():
	GPIO.setmode(GPIO.BCM)
	starttime = time.time()

	a = pm(4)
	b = pm(17)

	while True:
		while time.time() - starttime > 30:

			a.calc_particles()
			b.calc_particles()
			starttime = time.time()
		
		a.lowpulseoccupancy += a.read()
		b.lowpulseoccupancy += b.read()
		
if __name__ == '__main__':
	main()	
	