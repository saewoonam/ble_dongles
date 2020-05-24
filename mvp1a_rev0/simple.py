import serial
import glob
import time
import sys

new_dongle_port = glob.glob('/dev/tty.usbmodem*')
dongle_port = new_dongle_port[0]

if len(sys.argv)> 1:
    fname = sys.argv[1]
else:
    fname = 'encounters.dat'
f = open(fname, 'wb')
s = serial.Serial(dongle_port, baudrate=115200)
s.write(b's')  # stop data taking
print(s.readline())
# write file headers
s.write(b'u')
response = s.readline()
f.write(b"# "+response);
print('readback time: ', response)
msg = b"#  dongle_time, rssi, ch, mac, adv_packet"
padding = 99-len(msg);
msg = msg+b" "*padding + b"\n"
f.write(msg)
s.timeout = 1
s.write(b'g')
count = 0 
while True: 
    m = s.read(100)
    # print(count, len(m),m) 
    print("\r %5d"% count, end="")
    count += 1 
    if m.startswith(b'total_bytes'):
        break;
    f.write(m)
f.close()
s.close()
print(m)
