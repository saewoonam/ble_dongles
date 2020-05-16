import serial
import glob
import time
new_dongle_port = glob.glob('/dev/tty.usbmodem*')
dongle_port = new_dongle_port[0]

f = open('encounters.dat', 'wb')
s = serial.Serial(dongle_port)
# write file headers
s.write(b'u')
response = s.readline()
f.write(b"# "+response);
print('readback time: ', response)
msg = b"#  dongle_time, rssi, mac, adv_packet"
f.write(msg)

s.write(b'g')
count = 0 
while True: 
    m = s.readline()
    # print(count, len(m),m) 
    print("\r %5d"% count, end="")
    count += 1 
    if m.startswith(b'total_bytes'):
        break;
    f.write(m)
f.close()
s.close()
