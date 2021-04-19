from __future__ import print_function
import minimalmodbus
import time

# https://www.testequity.com/RS-232-F4-resources
# https://assets.testequity.com/te1/Documents/chambers/107man.pdf

class test_equity_107_usb():
	
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
		self.register_read_model            = 0
	
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
	
	def set_temp(self, target_temp, guardband=1, soak_time=1, stable_cnt=10):
		self.write_temp_value(temp)
		self.start_chamber()
		stable = False
		cnt    = 0
		print("Target temperature is " + str(target_temp) + ", Guardband is " + str(guardband))
		while not stable:
			time.sleep(1)
			current_temp = self.read_temp()
			print(current_temp)
			if (target_temp - guardband) <= current_temp <= (target_temp + guardband):
				cnt += 1
			else:
				cnt = 0
			if (cnt == stable_cnt):
				stable = True
		while soak_time >= 1.0:
			print("Wait {:0.2f} minutes before measurement...".format(soak_time))
			time.sleep(60)
			soak_time -= 1.0
		if soak_time > 0.0:
			time.sleep(60.0 * soak_time)
		print("Chamber is at temperature")
