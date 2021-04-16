from test_equity_107_usb import test_equity_107_usb
import time

tc = test_equity_107_usb(serial_port='/dev/ttyUSB0') # serial_port='COM6' for Windows
print(tc.read_temp())
tc.write_temp_value(24.7)
tc.start_chamber()
time.sleep(1)
tc.stop_chamber()
time.sleep(1)
tc.set_temp(26)
print("Temperature has now been reached")
