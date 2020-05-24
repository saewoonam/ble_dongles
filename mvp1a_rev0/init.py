import glob
import subprocess
import sys
import time
import serial

if len(sys.argv) > 1:
    print(sys.argv)
    do_flash = True
else:
    do_flash = False

def flash():
    dongle_port = glob.glob('/dev/tty.usbmodem*')

    print('Trying to program dongle on: ', dongle_port[0]);

    cmd = ['nrfutil',  'dfu',  'usb-serial',  '-pkg',  'bt_cdc_fs_ch.zip',  '-p', dongle_port[0]]
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
    return new_dongle_port[0]

if do_flash:
    dongle_port = flash()
else:
    new_dongle_port = glob.glob('/dev/tty.usbmodem*')
    dongle_port = new_dongle_port[0]

s = serial.Serial(dongle_port, timeout=2);
# Lets see what is on the flash
print('List files')
s.write(b'l')
start = time.time()
count = 0
while True:
    print(count, time.time(), s.readline())
    count += 1
    if time.time()-start > 10:
        print("Done waiting")
        break;
    if count == 3:
        print("Success");
        break;
#  Clear encounters file
print ("Clear encounters file")
s.write(b'c')
# setup time
print ("setup time")
t = int(time.time())
msg = b't'+t.to_bytes(4,'little')
s.write(msg)
time.sleep(0.5)
s.write(b'u')
response = s.readline()
print('readback time: ', response, 'computer sent: ', t)
s.close()
