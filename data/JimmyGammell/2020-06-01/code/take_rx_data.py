#%%
# -*- coding: utf-8 -*-

import serial
import os
import csv
import time

RX_COM = 'COM4'
num_trials = 250
output_filepath = r'C:/Users/jgamm/Desktop/rssi_measurement/2020-06-01/pcb/distance_blocked'
output_filename = r'3.00.csv'

EXPECTED_SENDER_ID = 1
EXPECTED_MESSAGE   = b'abcde'

RX = serial.Serial(RX_COM, 9600)
rssis = [-1.0]*num_trials
times = [-1.0]*num_trials

RX.write(b'\n')
_ = RX.readline()
initial_time = time.time()
for trial in range(num_trials):
    while True:
        time.sleep(.1)
        RX.write(b'\n')
        response = RX.readline()
        if response[0] == ord(b'y'):
            sender_id = int((response[1] << 8)| response[2])
            raw_rssi = int(response[3] << 8 | response[4])
            rssi = .5*float((raw_rssi & 0x7FFF) - (raw_rssi & 0x8000))
            message = response[5:-1]
            assert sender_id == EXPECTED_SENDER_ID
            assert message   == EXPECTED_MESSAGE
            rssis[trial] = rssi
            times[trial] = time.time() - initial_time
            print('Packet %d received. Message: %s. RSSI: %fdBm.'%(trial+1, message, rssi))
            break
        else:
            assert response[0] == ord(b'n')

RX.close()

with open(os.path.join(output_filepath, output_filename), 'w', newline='') as F:
    writer = csv.writer(F, delimiter=',')
    writer.writerow(['Time since first transmission (s)', 'RSSI (dB)'])
    for datapoint in range(num_trials):
        writer.writerow([times[datapoint], rssis[datapoint]])
