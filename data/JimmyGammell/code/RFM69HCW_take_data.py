#%%
# -*- coding: utf-8 -*-

# Purpose of script:
#   Transmit packets and record RSSI a given number of times, between two RFM69HCW 
#    radios.
#   Data is stored in CSV file.
# How to use:
#   Attach two arduinos programmed with rxtx_20dBm.ino, connected to RFM69HCW radios.
#   (filepath)/(filename) gives name of file to which data will be written.
#   ACK_CHAR and NACK_CHAR are used for communication with arduinos, and should
#    not be changed unless arduino code is changed to match - probably no reason
#    to change them.
#   TX_COM and RX_COM indicate ports to which transmitter and receiver RFM69HCWs 
#    are connected.
#   num_trials gives number of packets to transmit. Packets will be transmitted
#    repeatedly until successfully received.

ACK_CHAR = '\n'
NACK_CHAR = '\r'
TX_COM = 'COM6'
RX_COM = 'COM4'
num_trials = 250
filepath = r'C:/Users/jgamm/Desktop/rssi_measurement/data/orientation/rfm69hcw/pcb/exp_4'
filename = r'0deg.pickle'

import serial
import time
import numpy as np
import pickle
import os
import csv

class RFM69HCW:
    def __init__(self, ser, network_id, self_id, timeout=.1):
        assert network_id  == (network_id&0xFF)
        assert self_id == (self_id&0xFFFF)
        ser.timeout = timeout
        self.network_id = network_id
        self.id = self_id
        self.ser = ser
        self.timeout = timeout
        assert self.available()
        self.configure(network_id, self_id)
    def __del__(self):
        self.ser.close()
    def wait_for_response(self):
        t_0 = time.time()
        while (self.ser.in_waiting == 0) and (time.time()-t_0 < self.timeout):
            pass
        return self.ser.in_waiting != 0
    def read_string_until(self, char):
        chars = [self.ser.read()]
        while chars[-1] != char.encode('ascii'):
            chars.append(self.ser.read())
        return chars
    def available(self):
        assert self.ser.in_waiting == 0
        self.ser.write(''.join(['t', ACK_CHAR]).encode('ascii'))
        if not self.wait_for_response():
            return False
        else:
            assert self.read_string_until(ACK_CHAR)[0].decode() == ACK_CHAR
            return True
    def configure(self, network_id, self_id):
        assert self.ser.in_waiting == 0
        assert network_id == (network_id & 0xFF)
        assert self_id == (self_id & 0xFFFF)
        self.ser.write(''.join(['c', chr(network_id), chr(self_id >> 8), chr(self_id & 0xFF), ACK_CHAR]).encode('ascii'))
        assert self.wait_for_response()
        self.read_string_until(ACK_CHAR)
    def write_packet(self, target_id, packet):
        assert self.ser.in_waiting == 0
        assert target_id == (target_id & 0xFFFF)
        s = ''.join(['w', chr(target_id >> 8), chr(target_id & 0xFF), packet, ACK_CHAR]).encode('ascii')
        self.ser.write(s)
        assert self.wait_for_response()
        assert self.read_string_until(ACK_CHAR)[0].decode() == ACK_CHAR
    def read_packet(self):
        assert self.ser.in_waiting == 0
        s = ''.join(['r', ACK_CHAR]).encode('ascii')
        self.ser.write(s)
        assert self.wait_for_response()
        if self.ser.read() == NACK_CHAR.encode('ascii'):
            return False
        else:
            response = self.read_string_until(ACK_CHAR)
            sender_id = (ord(response[0]) << 8) | ord(response[1])
            rssi = (ord(response[2]) << 8) | ord(response[3])
            rssi = (rssi & 0x7FFF) - (rssi & 0x8000)
            message = response[4:-1]
            return {'Sender ID': sender_id, 'RSSI': .5*float(rssi), 'Message': message}
        
        
TX = RFM69HCW(serial.Serial(TX_COM, 9600), 0, 1, .1)
print('Configured transmitter')
RX = RFM69HCW(serial.Serial(RX_COM, 9600), 0, 2, .1)
print('Configured receiver')

num_attempts = 0
RSSI = np.array([None]*num_trials)
time_taken = np.array([None]*num_trials)
for trial in range(num_trials):
    packet = False
    message = chr(np.random.randint(np.max([ord(ACK_CHAR), ord(NACK_CHAR)]), 128))
    t_0 = time.time()
    while packet == False:
        num_attempts += 1
        TX.write_packet(RX.id, message)
        time.sleep(.1)
        packet = RX.read_packet()
    time_taken[trial] = time.time()-t_0
    assert packet['Message'][0].decode() == message
    assert packet['Sender ID'] == TX.id
    RSSI[trial] = packet['RSSI']
print('Trials complete.')
print('Proportion of transmissions received: %f'%(num_trials/num_attempts))
print('Mean RSSI: %f'%np.mean(RSSI))
print('Standard deviation of RSSI: %f'%np.std(RSSI))

# Exp. 1: rotate CCW
# Exp. 2: rotate CCW
# Exp. 3: rotate CCW, receiver wire away from transmitter
# Exp. 4: rotate CCW

with open(os.path.join(filepath, filename), 'w', newline='') as F:
    writer = csv.writer(F, delimiter=',')
    writer.writerow(['Time taken', 'RSSI'])
    for t, rssi in zip(time_taken, RSSI):
        writer.write_row([t, rssi])
    

del TX
print('Closed transmitter')
del RX
print('Closed receiver')