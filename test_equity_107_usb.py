from __future__ import print_function
import minimalmodbus
import time

# https://www.testequity.com/RS-232-F4-resources
# https://assets.testequity.com/te1/Documents/chambers/107man.pdf

class TestEquity107():
	
	def __init__(self, serial_port):
		self.nchannels                      = 1
		self.inst = minimalmodbus.Instrument(serial_port, self.nchannels) # serial_port = '/dev/ttyUSB0'
		self.inst.serial.baudrate           = 9600
		self.inst.serial.timeout            = 1.0
		self.register_read_act_temp         = 100
		self.register_read_act_humid        = 104
		self.register_set_static_temp       = 300
		self.register_set_static_humid      = 319
		self.register_set_cur_profile_temp  = 4122
		self.register_set_cur_profile_humid = 4123
		self.register_set_enable            = 2000
		delf.register_read_model            = 0
	
	def check_model(self):
		model_num = 0
		model_num = self.inst.read_register(self.register_read_model, 0)
		if (model_num == 5270):
			return 1
		else:
			return 0

	def read_temp(self):
		temp = self.inst.read_register(self.register_read_act_temp, 1, signed=True) # Registernumber, 1 decimal place
		return temp

	def write_temp_value(self, temp_set):
		self.inst.write_register(self.register_set_static_temp, temp_set, 1, signed=True) # Registernumber, value, number of decimals

	def start_chamber(self):
		self.inst.write_register(self.register_set_enable, 1, 0)

	def stop_chamber(self):
		self.inst.write_register(self.register_set_enable, 0, 0)

	def set_temp(self, temp, guardband=1, soak_time=1):
		upper_lim = temp + guardband
		lower_lim = temp - guardband
		current_temp = self.read_temp()
		stable = 0
		cnt    = 10
		self.write_temp_value(temp)
		self.start_chamber()
		print('Waiting for chamber stabilization')
		while stable == 0:
			print('.', )
			time.sleep(1)
			current_temp = self.read_temp()
			print(current_temp)
			if lower_lim <= current_temp <= upper_lim:
				i       = 0
				stb_cnt = 0
				while (i < cnt) and not stable:
					print('.', )
					time.sleep(10)
					stb_temp = self.read_temp()
					print(stb_temp)
					if lower_lim <= stb_temp <= upper_lim:  # loop to check if 10 reads in a row are within limits
						stb_cnt += 1
						i       += 1
						if (i == 10) & (stb_cnt == i):
							stable = 1
					else:
						i += 1
		while soak_time >= 1.0:
			print('Wait %d minute(s) before measurement...' % soak_time)
			time.sleep(60)
			soak_time -= 1.0
		if soak_time > 0.0:
			time.sleep(60.0 * soak_time)
		print("Measurement in progress...")

#oven = TestEquity107(serial_port='/dev/ttyUSB0')
#print(oven.read_temp())
#oven.write_temp_value(24.7)
#oven.start_chamber()
#oven.stop_chamber()
#time.sleep(1)
#oven.set_temp(26)

