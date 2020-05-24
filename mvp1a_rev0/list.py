import serial
import glob
import time
import sys

new_dongle_port = glob.glob('/dev/tty.usbmodem*')
dongle_port = new_dongle_port[0]

s = serial.Serial(dongle_port, baudrate=115200)
s.write(b'l')
start = time.time()
count = 0
while True:
    print(count, '%.2f'%time.time(), s.readline())
    count += 1
    if time.time()-start > 10:
        print("Done waiting")
        break;
    if count == 3:
        print("Success");
        break;

