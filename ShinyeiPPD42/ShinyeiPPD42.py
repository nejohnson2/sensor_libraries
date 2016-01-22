import RPi.GPIO as GPIO
import time, os, math
	
class Shinyei(object):

	def __init__(self, pin):
		self.pin = pin 			# pin for GPIO connection
		self.lpo = 0			# duration of low pulses
		self.start_ltime = 0	# initialize to zero to prevent start with low pulse
		self._start()			# initialize GPIO pin
		
	def _start(self):
		'''Setup the GPIO pins
		with callback function'''
		GPIO.setup(self.pin, GPIO.IN)
		GPIO.add_event_detect(self.pin, GPIO.BOTH, self._get_lpo)

	def _get_lpo(self, channel):
		'''Callback function when pin 
		changes	high or low'''

		current_time = time.time()	# get time when event happened

		if not GPIO.input(channel):
			'''Reading went low'''
			self.start_ltime = current_time					# start timer for low reading
		else:
			'''Reading went high'''
			if self.start_ltime != 0:
				self.lpo += current_time - self.start_ltime		# add time that was low

	def _calc_ratio(self, duration):
		'''calculate ratio of low pulse time to total time'''
		if self.lpo != 0:
			self.ratio = float(self.lpo) / float(duration)		# calculate percentage of pulses being low
		else:
			self.ratio = 0

	def _calc_concentration(self):
		'''calculate datasheet formula'''
		self.concentration = 1.1 * math.pow(self.ratio,3) - 3.8 * math.pow(self.ratio,2) + 520*self.ratio + 0.62

	def read(self, duration):
		'''Output results every 30s
		otherwise do nothing'''
		start_time = time.time()

		while time.time() - start_time < duration:
			time.sleep(1) # do nothing over duration time
		else:
			self._calc_ratio(duration)
			self._calc_concentration()
			self.results = [self.lpo, self.ratio, self.concentration]
			self.lpo = 0
			return self.results
		

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	t = Shinyei(18)
	while True:
		print t.read(30)

	GPIO.cleanup()	

