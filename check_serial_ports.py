# https://pyserial.readthedocs.io/en/latest/tools.html#module-serial.tools.list_ports

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))
