# testequity107
![picture](https://assets.testequity.com/te1/product-images/medium/107+1054-left-open.jpg)

Python class to control TestEquity 107 Benchtop Temperature Chamber (Environmental Chamber) using minimalmodbus and a usb-to-serial cable.

"check_serial_ports.py" should work on both Windows and Linux. This can be used to list all serial ports (my cable has a specific chipset, so I know which port it is connected to).
There is a "check_model" function in "test_equity_107_usb.py" which can also be used to ensure that the specified serial port is connecting to the temperature chamber device.
