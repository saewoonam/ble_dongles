import glob
import subprocess
import sys
import time
import serial

new_dongle_port = glob.glob('/dev/tty.usbmodem*')
dongle_port = new_dongle_port[0]
with open('encounters.dat', 'wb') as f:
    s = serial.Serial(dongle_port);
    s.write(b'u')
    response = s.readline()
    f.write(b"# "+response);
    print('readback time: ', response)
    msg = b"#  dongle_time, rssi, mac, adv_packet"
    f.write(msg)
    # Lets see what is on the flash
    s.write(b'f')
    print('flash info: ', s.readline())
    s.write(b'g')
    count = 0
    while True:
        response = s.readline()
        if len(response):
            print(count, s.readline())
            # f.write(response)
            # f.flush()
            count += 1
        else:
            break;

s.close()
