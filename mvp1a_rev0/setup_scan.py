import serial
import glob
import time
import sys

new_dongle_port = glob.glob('/dev/tty.usbmodem*')
dongle_port = new_dongle_port[0]
print(dongle_port)
s = serial.Serial(dongle_port, baudrate=115200)
s.write(b'x')
time.sleep(2)
interval = 0x100
window = 0x100
msg = b'v' + interval.to_bytes(2,'little') + window.to_bytes(2,'little') 
s.write(msg)
time.sleep(2)
s.write(b'y')

