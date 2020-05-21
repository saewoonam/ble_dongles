#  log data to file
#  First arg is name of the serial port that is connected to the dongle
#  2nd arg is the filename
#
#  Press ctrl-c to quit

#  Issues:
#
#   When quitting with Ctrl-c...  The serial communicaiton can get messed
#   up...  The next time you run the program it may hang   You need to ctrl-c
#   to quit.   And try again.  Things should get reset properly then.
#


import sys
import serial
import time


filename = sys.argv[2]
print(filename)
f = open(filename, 'w')
count = 0
header = "local_time, dongle_time, rssi, remote_mac, remote_adv\n"
f.write(header)

s = serial.Serial(sys.argv[1], timeout=1)
s.write(b'r')  #  Command to send data to serial port
try:
    while True:
        line = "%.2f, " % time.time()
        line = line
        line += s.readline().decode()
        if len(line) == 0:
            print("retry to reopen serial port")
            s.close()
            s = serial.Serial(sys.argv[1], timeout=1)

        parse = line.split(',')
        if len(parse) > 2:
            f.write(line)
            f.flush()
            print("%7d, %s\r" % (count, parse[2]), end="\r")
            sys.stdout.flush()
        count += 1

except KeyboardInterrupt:
    s.write(b'z')   #  Command to stop sending data to serial port
    s.close()
    f.close()

