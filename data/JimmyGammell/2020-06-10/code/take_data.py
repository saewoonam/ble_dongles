#%%
# -*- coding: utf-8 -*-

# Offsets:
#  Original whip: -12cm

import re
import serial
import os
import csv
import time

output_filepath = r'C:/Users/jgamm/Desktop/rssi_measurement/2020-06-10/data/original_whip/orientation_exp4'
output_filename = r'test.csv'
I_COM = r'COM11'
R_COM = r'COM12'
NUM_TRIALS = 50

Data = {'time_since_start': [],
        'time_taken': [],
        'conn_idx': [],
        'distance': [],
        'avg_distance': [],
        'event': [],
        'fo_i': [],
        'fo_r': [],
        'agc_i': [],
        'agc_r': [],
        'dqf': [],
        'ia_i': [],
        'ia_r': [],
        'i_rssi': [],
        'r_rssi': []}

I = serial.Serial(port=I_COM,
                  baudrate=9600,
                  parity=serial.PARITY_NONE,
                  bytesize=serial.EIGHTBITS,
                  stopbits=serial.STOPBITS_ONE)
R = serial.Serial(port=R_COM,
                  baudrate=9600,
                  parity=serial.PARITY_NONE,
                  bytesize=serial.EIGHTBITS,
                  stopbits=serial.STOPBITS_ONE)

try:
    I.flush()
    R.flush()
    trial = 0
    start_time = time.time()
    while True:
        while I.read() != b'M':
            pass # Wait for beginning of a transmission
        i_output = (I.readline()+I.readline()+I.readline()).decode('ascii')
        if 'distance: inf' in i_output: # Skip invalid measurements
            continue
        if not ('dqf: 100' in i_output): # Skip low-quality measurements
            continue
        output = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', i_output)
        assert len(output) == 14
        Data['time_since_start'].append(int(1000*(time.time()-start_time)))
        Data['time_taken'].append(int(output[0]))
        Data['conn_idx'].append(int(output[1]))
        Data['distance'].append(float(output[2]))
        Data['avg_distance'].append(float(output[3]))
        Data['event'].append(int(output[4]))
        Data['fo_i'].append(int(output[5]))
        Data['fo_r'].append(int(output[6]))
        Data['agc_i'].append(int(output[7]))
        Data['agc_r'].append(int(output[8]))
        Data['dqf'].append(int(output[9]))
        Data['ia_i'].append(int(output[10]))
        Data['ia_r'].append(int(output[11]))
        Data['i_rssi'].append(int(output[12]))
        Data['r_rssi'].append(int(output[13]))
        trial += 1
        if trial == NUM_TRIALS:
            break
finally:
    I.close()
    R.close()

with open(os.path.join(output_filepath, output_filename), 'w', newline='') as F:
    writer = csv.writer(F, delimiter=',')
    writer.writerow([index for index in Data])
    for trial in range(NUM_TRIALS):
        writer.writerow([Data[index][trial] for index in Data])
    
    