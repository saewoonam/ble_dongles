import glob
import subprocess
import sys
import time
import serial
dongle_port = glob.glob('/dev/tty.usbmodem*')

print('Trying to program dongle on: ', dongle_port[0]);

cmd = ['nrfutil',  'dfu',  'usb-serial',  '-pkg',  'check.zip',  '-p', dongle_port[0]]
process = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
# print(stdout, stderr)

# /dev/tty.usbmodemEEAD79D511BD1

if stdout==b'Device programmed.\n':
    print(stdout.decode())
    print('Success with flash')
else:
    print(stderr.decode())
    print('failed to flash')
    sys.exit(1)

while True:
    new_dongle_port = glob.glob('/dev/tty.usbmodem*')
    if len(new_dongle_port) > 0:
        if new_dongle_port[0] == dongle_port[0]:
            print('wait for update to port')
            time.sleep(1)
        else:
            break
print(' new dongle port: ', new_dongle_port[0])
  
s = serial.Serial(new_dongle_port[0], timeout=2);
count = 0
start = time.time()
while True:
    print(count, time.time(), s.readline())
    count += 1
    if time.time()-start > 10:
        print("Something failed")
        break;
    if count == 21:
        print("Success");
        break;

s.close()
