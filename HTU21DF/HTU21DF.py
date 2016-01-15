#!/usr/bin/python

import time
from Adafruit_I2C import Adafruit_I2C

class HTU21DF:
	i2c = None

	# Registers
	__HTU21DF_READTEMP	=	0xE3
	__HTU21DF_READHUM	=	0xE5
	__HTU21DF_READREG	=	0xE7
	__HTU21DF_RESET	 	=	0xFE

	# Constructor
	def __init__(self, address=0x40):
		self.i2c = Adafruit_I2C(address)
		self.begin()

	def begin(self):
		"""
		Initialize the module and reset
		"""
		self.reset()

		register = self.i2c.readList(self.__HTU21DF_READREG, 1)
		
		time.sleep(0.2)

		if register[0] == 2:
			return True
		
		return False

	def reset(self):
		"""
		Reset the module
		"""
		self.i2c.writeRaw8(self.__HTU21DF_RESET)

		time.sleep(0.2)


	def readTemperature(self):
		""" 
		Read raw temperature and
		convert to celcius

		byteArray[0], byteArray[1]: Raw temperature data
		byteArray[2] : CRC
		"""
		# byteArray = [0]*6
		# for i in range(len(data)):
		# 	data[i] = self.i2c.readU8()
			

		byteArray = self.i2c.readList(self.__HTU21DF_READTEMP, 3)
		print byteArray
		temp_reading = (byteArray[0] << 8) + byteArray[1]

		# Clear the status bits (maybe necessary)
		#temp_reading = temp_reading & 0xFFFC;

		temperature = ((temp_reading / 65536) * 175.72 ) - 46.85 # formula from datasheet

		return temperature

	def readHumidity(self):
		"""
		Read raw humidity and calculate
		humidity compensation

		byteArray[0], byteArray[1]: Raw relative humidity data
		byteArray[2] : CRC
		"""
		byteArray = self.i2c.readList(self.__HTU21DF_READHUM, 3)

		hum_reading = (byteArray[0] << 8) + byteArray[1]

		# Clear the status bits (maybe necessary)
		#hum_reading = hum_reading & 0xFFFC;

		humidity = ((hum_reading / 65536) * 125.0) - 6 # formula from datasheet
		
		# to get the compensated humidity we need to read the temperature
		# temperature = read_temperature()
		# humidity = ((25 - temperature) * -0.15) + humidity
		
		return humidity
		

