import RPi.GPIO as GPIO
import time, os, math
	
class Shinyei(object):

	def __init__(self, pin):
		self.pin = pin 			# pin for GPIO connection
		GPIO.setup(self.pin, GPIO.IN)
		
	def _start(self):
		'''Set default values and 
		attach event detection'''
		self.lpo = 0				# duration of low pulses
		self.start_ltime = 0		# initialize to zero to prevent start with low pulse
		GPIO.add_event_detect(self.pin, GPIO.BOTH, self._get_lpo)

	def _reset(self):
		'''Remove event detection'''
		GPIO.remove_event_detect(self.pin)	# prevents an interrupt during the rest of the code		

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
				duration = current_time - self.start_ltime		# add time that was low
				self.lpo += duration

	def _calc_ratio(self, duration):
		'''calculate ratio of low pulse time to total time'''
		if self.lpo != 0:
			ratio = float(self.lpo) / float(duration)		# calculate percentage of pulses being low
		else:
			ratio = 0

		return ratio

	def _calc_concentration(self, ratio):
		'''calculate particles per 0.01 cubic feet'''
		concentration = (1.1 * ratio**3) - (3.8 * ratio**2) + (520 * ratio) + 0.62

		return concentration

	def read(self, duration):
		'''Output results every 30s
		otherwise do nothing'''
		self._start()
		start_time = time.time()

		while time.time() - start_time < duration:
			pass			# do nothing 
		else:
			r = self._calc_ratio(duration)
			c = self._calc_concentration(r)

			self._reset()	# remove event detect
			return [self.lpo, r, c]
		

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	t = Shinyei(18)
	while True:
		print t.read(30)

	GPIO.cleanup()	

