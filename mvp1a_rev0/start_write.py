import serial
import glob
import time
new_dongle_port = glob.glob('/dev/tty.usbmodem*')
dongle_port = new_dongle_port[0]

s = serial.Serial(dongle_port)
# write file headers
s.write(b'w')
