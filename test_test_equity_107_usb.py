from test_equity_107_usb import test_equity_107_usb
import time

tc = test_equity_107_usb(serial_port='/dev/ttyUSB0') # serial_port='COM6' for Windows
print(tc.read_temp())
tc.write_temp_value(24.7)
tc.start_chamber()
time.sleep(1)
tc.stop_chamber()
time.sleep(1)
#show temp every 5 seconds, 21C target +/- 0.5C, soak for 0.5 minutes
tc.set_temp(target_temp=21, guardband=0.5, sample_interval=5, soak_time=0.5)
