import RPi.GPIO as GPIO
import time, math

class MCP3008:
	def __init__(self, SPICLK, SPIMISO, SPIMOSI, SPICS):
		self.SPICLK = SPICLK
		self.SPIMISO = SPIMISO
		self.SPIMOSI = SPIMOSI
		self.SPICS = SPICS
		self.setup()

	def setup(self):
		GPIO.setup(self.SPICLK, GPIO.OUT)
		GPIO.setup(self.SPIMISO, GPIO.IN)
		GPIO.setup(self.SPIMOSI, GPIO.OUT)
		GPIO.setup(self.SPICS, GPIO.OUT)

	def read(self, adcChannel, duration):
		starttime = time.time()
		sample_sum = 0
		dc_offset = 512
		num_samples = duration

		while time.time() - starttime < duration:
			GPIO.output(self.SPICS, True)

			GPIO.output(self.SPICLK, False)  # start clock low
			GPIO.output(self.SPICS, False)     # bring CS low
			
			commandout = adcChannel
			commandout |= 0x18		# start bit + single-ended bit
			commandout <<= 3		# ?

			for i in range(5):
				if(commandout & 0x80):
					GPIO.output(self.SPIMOSI, True)
				else:
					GPIO.output(self.SPIMOSI, False)

				commandout <<= 1
				GPIO.output(self.SPICLK, True)
				GPIO.output(self.SPICLK, False)

			adcout = 0

			# read in one empty bit, one null bit and 10 ADC bits
			for i in range(12):
				GPIO.output(self.SPICLK, True)
				GPIO.output(self.SPICLK, False)
				adcout <<=1
				if (GPIO.input(self.SPIMISO)):
					adcout |= 0x1

			GPIO.output(self.SPICS, True)
			adcout >>=1

			signal = adcout - dc_offset
			
			signal *= signal
			sample_sum += signal
			
		
		RMS = math.sqrt(sample_sum / num_samples)
		voltage = RMS / (3.3 / 1024.0)
		db = 20 * math.log10(RMS * (3.3 / 1024.0))
		return db


	def __del__(self):
		try:
			GPIO.cleanup()
		except:
			pass


if __name__ == "__main__":    
	GPIO.setmode(GPIO.BCM)
	SPICLK = 6
	SPIMISO = 13
	SPIMOSI = 19
	SPICS = 26

	a = MCP3008(SPICLK, SPIMISO, SPIMOSI, SPICS)

	while True:
		print a.read(7, 5) # adc pin and sample duration
		