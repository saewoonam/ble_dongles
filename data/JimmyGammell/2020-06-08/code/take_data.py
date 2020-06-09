#%%
# -*- coding: utf-8 -*-

# RSSI - I assume dBm? Not specified in wireless ranging SDK guide

import re
import serial
import os
import csv

output_filepath = r'C:/Users/jgamm/Desktop/rssi_measurement/2020-06-08/data/original_whip/orientation_exp4'
output_filename = r'360.csv'
I_COM = r'COM11'
R_COM = r'COM12'
NUM_TRIALS = 50
VERBOSE = False

Data = {'time taken': [],
        'BLE connection number': [],
        'distance': [],
        'average distance': [],
        'event': [],
        'initiator frequency offset': [],
        'reciever frequency offset': [],
        'initiator AGC gain': [],
        'reciever AGC gain': [],
        'distance quality factor': [],
        'initiator tone exchange steps': [],
        'reciever tone exchange steps': [],
        'initiator RSSI': [],
        'reciever RSSI': []}

Instigator = serial.Serial(port=I_COM,
                   baudrate=115200,
                   parity=serial.PARITY_NONE,
                   bytesize=serial.EIGHTBITS,
                   stopbits=serial.STOPBITS_ONE)

Reciever = serial.Serial(port=R_COM,
                   baudrate=115200,
                   parity=serial.PARITY_NONE,
                   bytesize=serial.EIGHTBITS,
                   stopbits=serial.STOPBITS_ONE)

try:
    Instigator.flush()
    trial = 0
    while True:
        while(Instigator.read(size=1) != b'M'): 
            pass
        rx_output = b''
        for i in range(3):
            rx_output += Instigator.readline()
        if re.findall(r'(inf)', rx_output.decode('ascii')) != []:
            if VERBOSE:
                print('Trial %d: error'%(trial+1))
            continue
        trial += 1
        output = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', rx_output.decode('ascii'))
        if len(output) < 14:
            if VERBOSE:
                print('Trial %d: error'%(trial))
            trial -= 1
            continue
        time_taken = int(output[0])
        conn_idx = int(output[1])
        distance = float(output[2])
        avg_distance = float(output[3])
        event = int(output[4])
        fo_i = int(output[5])
        fo_r = int(output[6])
        agc_i = int(output[7])
        agc_r = int(output[8])
        dqf = int(output[9])
        ia_i = int(output[10])
        ia_r = int(output[11])
        i_rssi = int(output[12])
        r_rssi = int(output[13])
        Data['time taken'].append(time_taken)
        Data['BLE connection number'].append(conn_idx)
        Data['distance'].append(distance)
        Data['average distance'].append(avg_distance)
        Data['event'].append(event)
        Data['initiator frequency offset'].append(fo_i)
        Data['reciever frequency offset'].append(fo_r)
        Data['initiator AGC gain'].append(agc_i)
        Data['reciever AGC gain'].append(agc_r)
        Data['distance quality factor'].append(dqf)
        Data['initiator tone exchange steps'].append(ia_i)
        Data['reciever tone exchange steps'].append(ia_r)
        Data['initiator RSSI'].append(i_rssi)
        Data['reciever RSSI'].append(r_rssi)
        if VERBOSE:
            print('Trial %d:'%(trial))
            print('\tTime taken: %dms'%(time_taken))
            print('\tBLE connection number: %d'%(conn_idx))
            print('\tDistance: %1.2fm'%(distance))
            print('\tAverage distance: %1.2fm'%(avg_distance))
            print('\tEvent: %d'%(event))
            print('\tInitiator frequency offset: %dkHz'%(fo_i))
            print('\tReciever frequency offset: %dkHz'%(fo_r))
            print('\tInitiator AGC gain: %d'%(agc_i))
            print('\tReciever AGC gain: %d'%(agc_r))
            print('\tDistance quality factor: %d'%(dqf))
            print('\tInitiator tone exchange steps: %d'%(ia_i))
            print('\tReciever tone exchange steps: %d'%(ia_r))
            print('\tInitiator RSSI: %d'%(i_rssi))
            print('\tReciever RSSI: %d'%(r_rssi))
        if trial > NUM_TRIALS:
            break
finally:
    Instigator.close()
    Reciever.close()

with open(os.path.join(output_filepath, output_filename), 'w', newline='') as F:
    writer = csv.writer(F, delimiter=',')
    writer.writerow(['time taken (ms)', 'distance (m)', 'avg. distance (m)', 
                     'initiator RSSI', 'reciever RSSI', 'BLE connection number',
                     'event', 'initiator frequency offset (kHz)', 'reciever frequency offset (kHz)',
                     'initiator AGC gain', 'reciever AGC gain', 'distance quality factor',
                     'initiator tone exchange steps', 'reciever tone exchange steps'])
    for i in range(NUM_TRIALS):
        row = [Data['time taken'][i], Data['distance'][i], Data['average distance'][i],
               Data['initiator RSSI'][i], Data['reciever RSSI'][i], Data['BLE connection number'][i],
               Data['event'][i], Data['initiator frequency offset'][i], Data['reciever frequency offset'][i],
               Data['initiator AGC gain'][i], Data['reciever AGC gain'][i], Data['distance quality factor'][i],
               Data['initiator tone exchange steps'][i], Data['reciever tone exchange steps'][i]]
        writer.writerow(row)